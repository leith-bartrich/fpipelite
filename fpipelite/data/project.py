from fpipelite.data.data import FindDataFromPath, Data, GenericAdapter, T
import uuid
import typing


class ProjectData(Data):

    pass



def FindProjectFromPath(path: str) -> (bool, ProjectData):
    """
    Does a reverse recursive search from the given path, to find any declared project.  The path can be a file path or directory.  It can be absolute or relative.
    :param path: the file or dir path from which to search
    :return: A tuple of type (bool,ApplicationData) where the bool indicates success or failure of the search, and the second value is either the loaded data, or None (if not found).
    """
    found, data, path = FindDataFromPath(path, "project")
    if found:
        return found, ProjectData(data, path)
    else:
        return found, None


def NewProject(path: str, short_name: str, long_name: str, id: uuid.UUID = None) -> ProjectData:
    data = ProjectData({}, path)

    short_name_adapter = ShortNameAdapter(data)
    long_name_adapter = LongNameAdapter(data)
    id_adapter = IDAdapter(data)

    short_name_adapter.set(short_name)
    long_name_adapter.set(long_name)

    if id == None:
        id_adapter.set(uuid.uuid4())
    else:
        id_adapter.set(id)

    return data


class ShortNameAdapter(GenericAdapter[str]):

    def get_keyname(self) -> str:
        return "short_name"


class LongNameAdapter(GenericAdapter[str]):

    def get_keyname(self) -> str:
        return "long_name"


class IDAdapter(GenericAdapter[uuid.UUID]):

    def get_keyname(self) -> str:
        return "id"

    def from_json(self, val) -> uuid.UUID:
        return uuid.UUID(val)

    def to_json(self, val: uuid.UUID):
        return str(val)
