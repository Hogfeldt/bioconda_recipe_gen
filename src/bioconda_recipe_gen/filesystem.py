import os


class Filesystem:
    def __init__(self, path):
        self._root_path = path
        self._root_dir = self.create_directory(path)
        self._files = self._root_dir.files
        self._directories = self._root_dir.directories

    def create_directory(self, path):
        files = []
        dirs = []
        for elem in os.listdir(path):
            elem_path = "%s/%s" % (path, elem)
            if os.path.exists(elem_path):
                if os.path.isfile(elem_path):
                    files.append(File(elem))
                else:
                    sub_dir = "%s/%s" % (path, elem)
                    dirs.append(self.create_directory(sub_dir))
        curr_dir_name = path.split("/")[-1]
        return Directory(
            curr_dir_name, files, dirs, path.replace(self._root_path, "", 1)
        )

    def is_file_in_root(self, search_file):
        return search_file in [f.name for f in self._files]

    def where_is_file_in_filesystem(self, search_file):
        return search_filesystem_for_file(self._root_dir, search_file)

    def get_dict_representation(self):
        """ Returns a dictionary representation of the FileSystem.
        For now only used to check that the correct Filesystem if created."""
        return self._root_dir.get_dict_representation()


class Directory:
    def __init__(self, name, files, dirs, path):
        self._name = name
        self._files = files
        self._directories = dirs
        self._path = path

    @property
    def name(self):
        return self._name

    @property
    def files(self):
        return self._files

    @property
    def directories(self):
        return self._directories

    @property
    def path(self):
        return self._path

    def get_dict_representation(self):
        dict_representation = dict()
        file_list = []
        for curr_file in self._files:
            file_list.append(curr_file.name)
        dict_representation["files"] = file_list
        for curr_dir in self.directories:
            dict_representation[curr_dir.name] = curr_dir.get_dict_representation()
        return dict_representation


class File:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


def search_filesystem_for_file(directory, search_file):
    paths = []
    print(directory._files)
    if search_file in [f.name for f in directory._files]:
        paths.append("%s/%s" % (directory._path, search_file))
    for curr_dir in directory._directories:
        paths.extend(search_filesystem_for_file(curr_dir, search_file))
    print(paths)
    return paths
