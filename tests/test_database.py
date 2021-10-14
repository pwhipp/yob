import os
import json
import hashlib

from tests.test_yobs import YobTestCase
from yob_database import YobDatabase


class TestYobDatabase(YobTestCase):
    animal_init = {'age': 0}
    cats_and_dogs = {'dog': ['fido', 'rover', 'spud'],
                     'cat': ['puss', 'ginger', 'oscar']}  # using <type>/<name> as uids

    def setUp(self):
        super().setUp()
        self.db = YobDatabase(self.root)

    def create_cats_and_dogs(self):
        for animal_type, animal_names in self.cats_and_dogs.items():
            for name in animal_names:
                uid = os.path.join(animal_type, name)
                data = {**self.animal_init, 'type': animal_type, 'name': name}

                self.db.create(uid, data)

    def test_database(self):
        self.create_cats_and_dogs()

        for animal_type, animal_names in self.cats_and_dogs.items():
            for name in animal_names:
                uid = os.path.join(animal_type, name)
                self.assertDictEqual(
                    {**self.animal_init, 'type': animal_type, 'name': name},
                    self.db.get(uid).data)

    def test_put(self):
        self.create_cats_and_dogs()

        uid = 'dog/fido'
        with self.db.get(uid) as fido:
            fido['age'] = 10

        self.assertEqual(self.db.get(uid)['age'], 10)

    def test_list(self):
        self.create_cats_and_dogs()
        expected_dog_hashes = {get_dict_hash({**self.animal_init, 'type': 'dog', 'name': name})
                               for name in self.cats_and_dogs['dog']}
        actual_dog_hashes = {get_dict_hash(dog.data) for dog in self.db.list('dog')}

        self.assertSetEqual(actual_dog_hashes, expected_dog_hashes)

    def test_filter(self):
        self.create_cats_and_dogs()

        all_ending_with_r = {yob['name']
                             for yob in self.db.filter(lambda y: y['name'].endswith('r'))}
        self.assertSetEqual({'rover', 'ginger', 'oscar'}, all_ending_with_r)

        all_cats_ending_with_r = {yob['name']
                                  for yob in self.db.filter(lambda y: y['name'].endswith('r'), 'cat')}
        self.assertSetEqual({'ginger', 'oscar'}, all_cats_ending_with_r)


def get_dict_hash(dictionary):
    return hashlib.sha256(bytes(repr(json.dumps(dictionary, sort_keys=True)), 'UTF-8')).hexdigest()