import pkg_resources


class BuildScript:
    """ Represents a build.sh """

    def __init__(self, path):
        self._path = path
        self._lines = list()
        build_template_file = pkg_resources.resource_filename(
            __name__, "recipes/template_build.sh"
        )
        with open(build_template_file, "r") as template:
            self._lines = template.readlines()

    @property
    def path(self):
        return self._path

    def write_build_script_to_file(self):
        """ Write build script to path/build.sh """
        lines_to_write = ['#!/bin/bash\n'] + self._lines
        with open("%s/build.sh"%self._path, 'w') as fp:
           fp.writelines(lines_to_write) 

    def add_cmake_flags(self, flags):
        """ Add flags to the cmake call """
        for i, line in enumerate(self._lines):
            if line.startswith("cmake .."):
                self._lines[i] = "cmake .. %s" % flags


