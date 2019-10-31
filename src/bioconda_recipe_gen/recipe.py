import logging
from os import listdir, getcwd, mkdir
from os.path import isfile, join, exists
import os

from . import make_dict
from .utils import copytree

build_tools = ["cmake", "make", "autoconf"]
libs = ["hdf5", "zlib"]


class Recipe:
    """ Represents a meta.yaml recipe file """

    def __init__(self, name, version, path=None):
        self.recipe_dict = {"package": {"name": name, "version": version}}
        if path is None:
            self._path = os.path.join(getcwd(), name)
        else:
            self._path = path

    def __eq__(self, other):
        """ Overwrite default implementation. Compare recipe_dict instead of id """
        if isinstance(other, Recipe):
            return self.recipe_dict == other.recipe_dict
        return False

    @property
    def name(self):
        return self.recipe_dict["package"]["name"]

    @name.setter
    def name(self, name):
        self.recipe_dict["package"]["name"] = name

    @property
    def path(self):
        return self._path

    @property
    def test_commands(self):
        try:
            return self.recipe_dict["test"]["commands"]
        except KeyError:
            return []

    @property
    def url(self):
        return self.recipe_dict["source"]["url"]

    def increment_build_number(self):
        build_number = self.recipe_dict["build"]["number"]
        self.recipe_dict["build"]["number"] = int(build_number) + 1
        self.write_recipe_to_meta_file()

    def write_recipe_to_meta_file(self):
        """ Writes the current recipe_dict into the meta.yaml file """
        if exists(self._path) is False:
            mkdir(self._path)
        make_dict.make_meta_file_from_dict(
            self.recipe_dict, os.path.join(self._path, "meta.yaml")
        )

    def add_build_number(self, number):
        build = self.recipe_dict.setdefault("build", dict())
        build["number"] = number

    def add_source_url(self, url):
        source = self.recipe_dict.setdefault("source", dict())
        source["url"] = url

    def add_checksum_md5(self, checksum):
        source = self.recipe_dict.setdefault("source", dict())
        source["md5"] = checksum

    def add_checksum_sha256(self, checksum):
        source = self.recipe_dict.setdefault("source", dict())
        source["sha256"] = checksum

    def add_requirement(
        self, pack_name, type_of_requirement, debug_message="Not specified"
    ):
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
        requirements = self.recipe_dict.setdefault("requirements", dict())
        curr_list = requirements.setdefault(type_of_requirement, [])
        if pack_name not in curr_list:
            logging.debug(
                "Adding %s to %s. Reason for adding requirement: %s"
                % (pack_name, type_of_requirement, debug_message)
            )
            curr_list.append(pack_name)
            if type_of_requirement == "host":
                self.add_requirement(pack_name, "run")
            if (
                pack_name == "{{ compiler('cxx') }}"
                and "{{ compiler('c') }}" in curr_list
            ):
                curr_list.remove("{{ compiler('c') }}")

    def add_test_files_with_path(self, test_path):
        """ Adds test files from test_path to 'test: files: ... ' in recipe """
        if exists(self._path) is False:
            mkdir(self._path)
        copytree(test_path, self._path)
        if test_path is not None:
            files = [
                f
                for f in listdir(test_path)
                if isfile(join(test_path, f)) and "run_test." not in f
            ]
            test = self.recipe_dict.setdefault("test", dict())
            curr_list = test.setdefault("files", [])
            for f in files:
                curr_list.append(f)

    def add_test_files_with_list(self, test_files):
        """ Adds test files from test_files to the recipe """
        test = self.recipe_dict.setdefault("test", dict())
        curr_list = test.setdefault("files", [])
        for test_file in test_files:
            curr_list.append(test_file)

    def add_test_commands(self, commands):
        """ Adds test commands to 'test: commands: ... ' in recipe """
        test = self.recipe_dict.setdefault("test", dict())
        curr_list = test.setdefault("commands", [])
        if commands not in curr_list:
            curr_list.extend(commands)

    def add_patches(self, patches_path):
        """ Adds patches to 'source: patches: ... ' in recipe """
        if exists(self._path) is False:
            mkdir(self._path)
        copytree(patches_path, self._path)
        test = self.recipe_dict.setdefault("source", dict())
        curr_list = test.setdefault("patches", [])
        for f in listdir(patches_path):
            curr_list.append(f)
