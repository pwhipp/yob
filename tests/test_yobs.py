import os
from tempfile import TemporaryDirectory

from unittest import TestCase

from yob import Yob


class YobTestCase(TestCase):
    def setUp(self):
        self.temporary_directory = TemporaryDirectory(prefix='test_yobs_')
        self.root = self.temporary_directory.name

    def tearDown(self):
        self.temporary_directory.cleanup()


class TestYobs(YobTestCase):
    def test_yob(self):
        # Make one and save it
        filename = os.path.join(self.root, 'test_yob1')
        yob = Yob(filename)
        yob['type'] = 'dog'
        yob.update({'name': 'fido'})
        yob.save()
        self.assertDictEqual(yob.data, {'name': 'fido', 'type': 'dog'})

        # Load the one we made and check it
        yob_copy = Yob(filename)
        self.assertDictEqual(yob_copy.data, yob.data)

        # Change it and save it again
        yob['age'] = 20
        yob['name'] = 'fido (snr)'
        yob.save()

        yob_copy.load()
        self.assertDictEqual(yob_copy.data, {'name': 'fido (snr)', 'type': 'dog', 'age': 20})

        # Delete it
        yob_filename = yob.filename
        self.assertTrue(os.path.isfile(yob_filename))
        yob.delete()
        self.assertFalse(os.path.isfile(yob_filename))

    def test_yob_as_context(self):
        filename = os.path.join(self.root, 'test_yob2')
        with Yob(filename) as yob:
            yob.update({'age': 42})

        yob_copy = Yob(filename)
        self.assertDictEqual(yob_copy.data, {'age': 42})
