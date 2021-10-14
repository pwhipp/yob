import os

import yaml

from collections import UserDict
from contextlib import AbstractContextManager


class Yob(UserDict, AbstractContextManager):
    """
    YAML object: A dictionary that may persist as a file.
    """
    def __init__(self, filename, loader=None, updates=None):
        super().__init__()
        self.filename = filename
        self.loader = yaml.FullLoader if loader is None else loader
        if self.has_file:
            self.load()
        if updates:
            self.update(updates)

    def __exit__(self, __exc_type, __exc_value, __traceback):
        if __exc_type is None:
            self.save()
        return super().__exit__(__exc_type, __exc_value, __traceback)

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            return None

    @property
    def has_file(self):
        return os.path.isfile(self.filename)

    def load(self):
        with open(self.filename) as f:
            self.data = yaml.load(f, Loader=self.loader)

    def save(self):
        with open(self.filename, 'w') as f:
            if self.data:
                yaml.dump(self.data, f, width=128, indent=2)
                return
            if self.has_file:
                os.remove(self.filename)

    def delete(self):
        return os.unlink(self.filename)
