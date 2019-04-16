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
        mini_proc = build.mini_iterative_build(name)
        print("mini_proc return code:", mini_proc.returncode)
        for line in mini_proc.stdout.split("\n"):
            print(line)

        # Sanity check
        success = build.mini_sanity_check(bioconda_recipe_path, name)
        if success:
            print("SUCCESS: Package was successfully build")
        else:
            print("ERROR: Didn't pass the sanity check!")

        # copy the final recipe into the current directory
        copyfile(path + "/meta.yaml", "./meta.yaml")

    finally:
        # clean up
        rmtree(path)
        # Only for development
        rmtree('./%s' % name)
