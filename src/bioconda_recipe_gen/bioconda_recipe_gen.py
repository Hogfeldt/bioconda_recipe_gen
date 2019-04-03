import os
import sys
from shutil import copyfile, rmtree
import pkg_resources

from . import build


def return_hello():
    """ This is a test function for our unittest setup and should be removed when we start using the test setup"""
    return "hello"


def main(bioconda_recipe_path):
    # Setup variables
    name = "kallisto2"
    src = "https://github.com/pachterlab/kallisto/archive/v0.45.0.tar.gz"

    try:
        proc, dependencies = build.bioconda_utils_iterative_build(bioconda_recipe_path, name)

        # TODO: Try to iterate alpine image build
        proc, dependencies = build.alpine_iterative_build(src)
        for line in proc.stdout.split("\n"):
            print(line)

        proc = build.bioconda_utils_build(name, bioconda_recipe_path)
        for line in proc.stdout.split("\n"):
            print(line)
    finally:
        # clean up
        rmtree(path)
