import logging
from os import listdir
from os.path import isfile, join

from . import make_dict

build_tools = ["cmake", "make", "autoconf"]
libs = ["hdf5", "zlib"]


class Recipe:
    """ Represents a meta.yaml recipe file """

    def __init__(self, name, version, hashing):
        self.recipe_dict = dict()
        self.recipe_dict["package"]["name"] = name
        self.recipe_dict["package"]["version"] = version

    def __eq__(self, other):
        """ Overwrite default implementation. Compare recipe_dict instead of id """
        if isinstance(other, Recipe):
            return self.recipe_dict == other.recipe_dict
        return False

    def add_meta_file_path(self, path)
        self.path_to_meta_file = path_to_meta_file

    def write_recipe_to_meta_file(self):
        """ Writes the current recipe_dict into the meta.yaml file """
        make_dict.make_meta_file_from_dict(self.recipe_dict, self.path_to_meta_file)

    def add_source_url(self, url)
        self.recipe_dict["source"]["url"] = url

    def add_checksum_md5(self, checksum):
        self.recipe_dict["source"]["md5"] = checksum

    def add_checksum_sha256(self, checksum):
        self.recipe_dict["source"]["sha256"] = checksum

    def add_requirement(self, pack_name, type_of_requirement, debug_message = "Not specified"):
        """ Adds a package to the list of requirements in the recipe

        Args:
            pack_name: Name of the package to add
            type_of_requirement: Specify were you want to add the package "host", "build" or "run"
            debug_message: A message explaining why the package was added as a requirement
        """
        if type_of_requirement == "build" and pack_name in libs:
            return
        elif type_of_requirement == "host" and pack_name in build_tools:
            return
        curr_list = self.recipe_dict["requirements"].setdefault(type_of_requirement, [])
        if pack_name not in curr_list:
            logging.debug("Adding %s to %s. Reason for adding requirement: %s" % (pack_name, type_of_requirement, debug_message))
            curr_list.append(pack_name)
            if type_of_requirement == "host":
                self.add_requirement(pack_name, "run")

    def add_tests(self, test_path):
        """ Adds test files from test_path to 'test: files: ... ' in recipe """
        if test_path is not None:
            files = [
                f
                for f in listdir(test_path)
                if isfile(join(test_path, f)) and "run_test." not in f
            ]
            curr_list = self.recipe_dict["test"].setdefault("files", [])
            for f in files:
                curr_list.append(f)

    def add_test_command(self, command):
        """ Adds a test command to 'test: commands: ... ' in recipe """
        curr_list = self.recipe_dict["test"].setdefault("commands", [])
        if command not in curr_list:
            curr_list.append(command)

