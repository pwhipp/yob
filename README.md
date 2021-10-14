# Yobs: Python dictionaries that you can easily save, restore and edit as files

A Yob (yaml file object) is a python dictionary that you can easily save, restore and edit as a file.

Yobs also come with an optional simple but powerful file oriented database.

Yobs can be arbitrarily complex and may leverage the serialization/deserialization capabilities of [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) if needed.

While yobs are reasonably performant they are individual [yaml](https://yaml.org/) files at heart.

Specialize yobs to serve up JSON or models with any behavior based upon their data that you fancy.

Not tested on Windows.

## Use a lonely yob for configuration
```
In [1]: from yob import Yob

In [2]: y = Yob('/tmp/yobs/A')

# Use a context manager to automatically save any changes
In [3]: with y:
   ...:     y['base_path'] = '/tmp/yobs'
   ...: 

In [4]: y
Out[4]: {'base_path': '/tmp/yobs'}

# ...or explicitly save after changes
In [5]: y['max'] = 99

In [6]: y.save()

In [7]: y
Out[7]: {'base_path': '/tmp/yobs', 'max': 99}

# Use it like any other dictionary
In [8]: y['max']
Out [8]: 99
```

You can also edit the file directly - it is just [yaml](https://yaml.org/).

## Or put convivial yobs together as a file based database
The database is created from a root folder. Sub folders are generated from the unique identifier used for each yob in the database to make listing and filtering easy.

```

In [1]: animal_init = {'age': 0}

In [2]: cats_and_dogs = {'dog': ['fido', 'rover', 'spud'],
   ...:                  'cat': ['puss', 'ginger', 'oscar']}  # using <type>/<name> as uids
   
In [3]: from yob_database import YobDatabase

In [4]: !mkdir /tmp/test_yobs

In [5]: db = YobDatabase('/tmp/test_yobs')

In [6]: for animal_type, animal_names in cats_and_dogs.items():
   ...:     for name in animal_names:
   ...:         uid = f"{animal_type}/{name}"
   ...:         data = {**animal_init, 'type': animal_type, 'name': name}
   ...:         db.create(uid, data)
   ...:
In [7]: with db.get('dog/fido') as fido:
   ...:     fido['age'] = 10
   ...: 

In [8]: db.list()
Out[8]: 
[{'age': 0, 'name': 'oscar', 'type': 'cat'},
 {'age': 0, 'name': 'puss', 'type': 'cat'},
 {'age': 0, 'name': 'ginger', 'type': 'cat'},
 {'age': 0, 'name': 'rover', 'type': 'dog'},
 {'age': 0, 'name': 'spud', 'type': 'dog'},
 {'age': 10, 'name': 'fido', 'type': 'dog'}]

In [9]: db.filter(lambda y: y['name'].endswith('r'))
Out[9]: 
[{'age': 0, 'name': 'oscar', 'type': 'cat'},
 {'age': 0, 'name': 'ginger', 'type': 'cat'},
 {'age': 0, 'name': 'rover', 'type': 'dog'}]

In [10]: db.filter(lambda y: y['name'].endswith('r'), 'cat')
Out[10]: 
[{'age': 0, 'name': 'oscar', 'type': 'cat'},
 {'age': 0, 'name': 'ginger', 'type': 'cat'}]

In [11]: db.filter(lambda y: y['age'] > 5)
Out[11]: [{'age': 10, 'name': 'fido', 'type': 'dog'}]

```

The file structure is simple and easy to work with directly too:
```
(yob) test_yobs $ tree
.
├── cat
│   ├── ginger
│   ├── oscar
│   └── puss
└── dog
    ├── fido
    ├── rover
    └── spud

2 directories, 6 files
(yob) test_yobs $ cat cat/ginger
age: 0
name: ginger
type: cat
```