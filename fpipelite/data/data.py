import json
import os
import pathlib
import atomicfile
import rx
import rx.subject
import typing



class Data(object):
    _data = None
    _path = None

    def __init__(self, data: dict, path: str):
        self._data = data
        self._path = path

    def save(self):
        with atomicfile.AtomicFile(self._path, 'w') as f:
            json.dump(self.json_data, f, indent=4, sort_keys=True)

    @property
    def json_data(self) -> dict:
        return self._data

    def get_dir_path(self) -> str:
        return os.path.dirname(self.get_fpipelite_dir_path())

    def get_fpipelite_dir_path(self) -> str:
        return os.path.dirname(self._path)


_FPipeLiteDirName = ".fpipelite"
_FPipeLiteDataFileSuffix = "fpipelite.json"

def FindDataFromPath(path: str, typename: str) -> (bool, dict, str):
    """
    Does a reverse recursive search from the given path, to find any declared data.  The path can be a file path or directory.  It can be absolute or relative.
    :param path: the file or dir path from which to search
    :param typename:  the string typename of the data to load .e.g "project"
    :return: A tuple of type (bool,Data) where the bool indicates success or failure of the search, and the second value is either the loaded data, or None (if not found).
    """
    # relative handler
    if not os.path.isabs(path):
        return FindDataFromPath(os.path.abspath(path), typename)

    # file handler
    if os.path.isfile(path):
        (dir, fname) = os.path.split(path)
        return FindDataFromPath(dir, typename)

    # handle directory
    if os.path.isdir(path):
        if not os.path.exists(path):
            return False, None, ""
        else:
            litedir = os.path.join(path, _FPipeLiteDirName)
            if os.path.exists(litedir):
                loaded, data, fname = LoadDataFromDir(litedir, typename)
                if (loaded):
                    # succesful load, we return it
                    return True, data, fname

            # we get here if there's no lite dir, or if we didn't load a data succesfully

            # we try to do the parent
            dir, fname = os.path.split(path)
            if (dir == path):
                # we can't go higher
                return False, None, dir
            # may need to detect top of heirarchy here...
            return FindDataFromPath(dir, typename)

    # unhandled thing
    return False, None

def FPipeLiteDataFilenameFromType(typename: str):
    return typename.lower() + "." + _FPipeLiteDataFileSuffix

def LoadDataFromDir(path: str, typename: str) -> (bool, dict, str):
    """
    Loads project data from a directory.  By looking for '[typename].fpipelite.json' files and loading them.
    :param path: a path to the directory to search in.
    :return: an ApplicationData object
    """

    # check dir is legal and such
    if not os.path.isdir(path):
        raise NotADirectoryError(str)
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    fname = os.path.join(path, FPipeLiteDataFilenameFromType(typename))

    if not os.path.exists(fname):
        return False, None, fname

    if not os.path.isfile(fname):
        return False, None, fname

    f = open(fname, 'r')
    data = json.load(f)

    # TODO:  Check version and do any transform of old versions etc.
    # TODO:  Check for a redirect (such as to a network server) and execute it.

    f.close()

    # return data
    return True, data, fname

T = typing.TypeVar ('T')


class GenericAdapter(typing.Generic[T]):

    _data: Data = None
    _subject: rx.subject.BehaviorSubject = None

    def __init__(self, data: Data):
        self._data = data
        self._subject = rx.subject.BehaviorSubject(self.get())

    def navigate_to_dict(self) -> dict:
        return self._data.json_data

    def get_keyname(self) -> str:
        raise NotImplementedError

    def from_json(self, val) -> T:
        return val

    def to_json(self, val:T):
        return val

    def get(self) -> T:
        d = self.navigate_to_dict()
        if self.get_keyname() in d:
            v = d[self.get_keyname()]
            return self.from_json(v)
        else:
            return None

    def set(self, val: T):
        d = self.navigate_to_dict()
        v = self.to_json(val)
        d[self.get_keyname()] = v
        self._subject.on_next(val)

    def get_subject(self) -> rx.subject.BehaviorSubject:
        return self._subject

