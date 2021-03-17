import os
from fpipelite.data.data import FindDataFromPath, Data, GenericAdapter, T
import uuid
import typing


class WorkspaceData(Data):

    @property
    def short_name(self):
        parent, dirname = os.path.split(self.get_dir_path())
        return dirname


def FindWorkspaceFromPath(path: str) -> (bool, WorkspaceData):
    """
    Does a reverse recursive search from the given path, to find any declared project.  The path can be a file path or directory.  It can be absolute or relative.
    :param path: the file or dir path from which to search
    :return: A tuple of type (bool,ApplicationData) where the bool indicates success or failure of the search, and the second value is either the loaded data, or None (if not found).
    """
    found, data, path = FindDataFromPath(path, "workspace")
    if found:
        return found, WorkspaceData(data, path)
    else:
        return found, None

class IDAdapter(GenericAdapter[uuid.UUID]):

    def get_keyname(self) -> str:
        return "id"

    def from_json(self, val) -> uuid.UUID:
        return uuid.UUID(val)

    def to_json(self, val: uuid.UUID):
        return str(val)


def FindWorkspacesInPath(path: str, depth_limit=-1) -> [WorkspaceData]:
    """
    Recursively looks for workspaces in subdirectories and returns them all, up to the depth_limit of subdirectories.
    Since there is no such thing
    :param path: the directory from which to start searching.
    :param depth_limit: the limit of subdiriectories to seach.  -1 means no limit.
    :return: a list of WorkspaceData that was found and loaded
    """

    ret = []

    # if we were called with a limit of 0 we return empty.
    if (depth_limit == 0):
        return ret

    entries = os.listdir(path)

    # are we a workspace?
    found, data = FindWorkspaceFromPath(path)
    if found:
        # if so, we return our data and descend no further
        ret.append(data)
        return ret

    # we collect and return our subdirs' workspaces
    for entry in entries:
        if os.path.isdir(os.path.join(path, entry)):
            found_assets = FindWorkspacesInPath(os.path.join(path, entry), depth_limit - 1)
            ret.extend(found_assets)

    return ret



def NewWorkspace(path: str, id: uuid.UUID = None) -> WorkspaceData:
    data = WorkspaceData({}, path)

    id_adapter = IDAdapter(data)

    if id == None:
        id_adapter.set(uuid.uuid4())
    else:
        id_adapter.set(id)

    return data
