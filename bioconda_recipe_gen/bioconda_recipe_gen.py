import subprocess
import os
import sys
from shutil import copyfile, rmtree

from make_dict import make_dict_from_meta_file, make_meta_file_from_dict
from build import bioconda_utils_build

# TODO: Move this class to its own file. The file could be called something like recipe-handler.py
class Recipe:
    """ Represents a meta.yaml recipe file """

    def __init__(self, path_to_meta_file):
        self.path_to_meta_file = path_to_meta_file

        self.recipe_dict = make_dict_from_meta_file(path_to_meta_file)

    def write_recipe_to_meta_file(self):
        """ Writes the current recipe_dict into the meta.yaml file """
        make_meta_file_from_dict(self.recipe_dict, self.path_to_meta_file)

    def add_requirement(self, pack_name, type_of_requirement):
        """ Adds a package to the list of requirements in the recipe

        Args:
            pack_name: Name of the package to add
            type_of_requirement: Specify were you want to add the package "host", "build" or "run"
        """
        if self.recipe_dict["requirements"][type_of_requirement]:
            self.recipe_dict["requirements"][type_of_requirement].append(pack_name)
        else:
            self.recipe_dict["requirements"][type_of_requirement] = [pack_name]


def return_hello():
    """ This is a test function for our unittest setup and should be removed when we start using the test setup"""
    return "hello"


def main():
    # Setup variables
    name = "kallisto2"
    src = "https://github.com/pachterlab/kallisto/archive/v0.45.0.tar.gz"
    path = "../bioconda-recipes/recipes/" + name
    os.mkdir(path)

    # Copy recipe to into Bioconda
    copyfile("./recipes/meta.yaml", path + "/meta.yaml")
    copyfile("./recipes/build.sh", path + "/build.sh")

    recipe = Recipe(path + "/meta.yaml")

    proc = bioconda_utils_build(name)
    print("return code: " + str(proc.returncode) + "\n")
    if proc.returncode != 0:
        # Check for dependencies
        for line in proc.stdout.split("\n"):
            line_norma = line.lower()
            if "missing" in line_norma:
                print(line_norma)
                if "hdf5" in line_norma:
                    recipe.add_requirement("hdf5", "host")

        # after new requirements are added: write new recipe to meta.yaml
        recipe.write_recipe_to_meta_file()
    else:
        print("Build succeded")
        sys.exit(0)

    # TODO: Try to build with with alpine image


    proc = bioconda_utils_build(name, wd)
    for line in proc.stdout.split("\n"):
        print(line)

    # clean up
    rmtree(path)


if __name__ == "__main__":
    main()
