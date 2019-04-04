import os
import sys
from shutil import copyfile, rmtree
import pkg_resources

from . import build
from . import utils
from .recipe import Recipe


def return_hello():
    """ This is a test function for our unittest setup and should be removed when we start using the test setup"""
    return "hello"


def main(bioconda_recipe_path):
    # Setup variables
    name = "kallisto2"
    src = "https://github.com/pachterlab/kallisto/archive/v0.45.0.tar.gz"
    path = "%s/recipes/%s" % (bioconda_recipe_path, name)

    try:
        bioconda_proc, bioconda_dependencies = build.bioconda_utils_iterative_build(bioconda_recipe_path, name)

        # TODO: Try to iterate alpine image build
        alpine_proc, alpine_build_dependencies = build.alpine_iterative_build(src)
        for line in alpine_proc.stdout.split("\n"):
            print(line)

        alpine_run_proc, alpine_run_dependencies = build.alpine_run_test(src, alpine_build_dependencies, "kallisto --version")
        print("Alpine_run_proc:", alpine_run_proc)

        # Create recipe from the dependencies
        recipe = Recipe(path + "/meta.yaml")

        for dep in bioconda_dependencies:
            recipe.add_requirement(dep, "host")

        for dep in alpine_build_dependencies:
            conda_pkg_name = utils.map_alpine_pkg_to_conda_pkg(dep)
            if conda_pkg_name is None:
                print("ERROR: couldn't find an equivalent conda package to %s" % dep)
                continue
            # TODO: how do we know which type of requirement it is?
            recipe.add_requirement(conda_pkg_name, "host")
            recipe.add_requirement(conda_pkg_name, "build")

        for dep in alpine_run_dependencies:
            conda_pkg_name = utils.map_alpine_pkg_to_conda_pkg(dep)
            if conda_pkg_name is None:
                print("ERROR: couldn't find an equivalent conda package to %s" % dep)
                continue
            recipe.add_requirement(conda_pkg_name, "run") 
        
        recipe.write_recipe_to_meta_file()

        # Sanity check
        proc = build.bioconda_utils_build(name, bioconda_recipe_path)
        for line in proc.stdout.split("\n"):
            print(line)

        # copy the final recipe into the current directory
        copyfile(path + "/meta.yaml", "./meta.yaml")

    finally:
        # clean up
        rmtree(path)
