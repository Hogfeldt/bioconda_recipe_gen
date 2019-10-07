import pkg_resources
import os

from .utils import is_file_in_folder


class BuildScript:
    """ Represents a build.sh """

    def __init__(self, name, path):
        self.name = name
        self._path = path
        self._lines = list()
        build_template_file = pkg_resources.resource_filename(
            __name__, "recipes/template_build.sh"
        )
        with open(build_template_file, "r") as template:
            self._lines = template.readlines()
        source_code_dir = "%s/%s_source" % (os.getcwd(), name)
        if is_file_in_folder("configure.ac", source_code_dir):
            self.autoreconf_instead_of_cmake()

    def __eq__(self, other):
        """ Overwrite default implementation. Compare _lines instead of id """
        if isinstance(other, BuildScript):
            return self._lines == other._lines
        return False

    @property
    def path(self):
        return self._path

    def write_build_script_to_file(self):
        """ Write build script to path/build.sh """
        lines_to_write = ['#!/bin/bash\n'] + self._lines
        with open("%s/build.sh" % self._path, 'w') as fp:
            fp.writelines(lines_to_write)

    def add_cmake_flags(self, flags):
        """ Add flags to the cmake call """
        for i, line in enumerate(self._lines):
            if line.startswith("cmake .."):
                self._lines[i] = "cmake .. %s\n" % flags

    def add_moving_bin_files(self):
        """ Add lines to make sure the bin files are moved """
        self._lines.append("mkdir -p $PREFIX/bin\n")
        self._lines.append("cp bin/%s $PREFIX/bin\n" % self.name)

    def autoreconf_instead_of_cmake(self):
        print(self._lines)
        self._lines.insert(0, "./configure --prefix=$PREFIX\n")
        self._lines.insert(0, "autoreconf -fi\n")
        self._lines.remove("mkdir -p build\n")
        self._lines.remove("cd build\n")
        self._lines.remove("cmake ..\n")
