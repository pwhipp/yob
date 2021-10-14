import os
from yob import Yob


class YobDatabase:
    """
    A database of yobs.
    Each yob must have a UID which can be made up of anything that can go into a pathname.
    """
    def __init__(self, root):
        self.root = root

    def yob_filename(self, uid):
        return os.path.join(self.root, f"{uid}")

    def create(self, uid, initial_data):
        os.makedirs(os.path.dirname(self.yob_filename(uid)), exist_ok=True)

        with self.get(uid) as yob:
            yob.update(initial_data)

    def get(self, uid):
        return Yob(self.yob_filename(uid))

    @staticmethod
    def put(yob):  # syntactic sugar
        return yob.save()

    @staticmethod
    def delete(yob):  # syntactic sugar plus a bit of clean up
        folder = os.path.dirname(yob.filename)
        result = yob.delete()
        if not any(os.scandir(folder)):
            os.unlink(folder)
        return result

    def list(self, path=None):
        path = self.root if path is None else os.path.join(self.root, path)
        return self._list(path)

    def _list(self, path):
        result = []
        with os.scandir(path) as iterator:
            for dir_entry in iterator:
                if dir_entry.is_file():
                    result.append(Yob(dir_entry.path))
                elif dir_entry.is_dir():
                    result = result + self._list(dir_entry.path)
        return result

    def filter(self, fn, path=None):
        return [yob for yob in self.list(path) if fn(yob)]
