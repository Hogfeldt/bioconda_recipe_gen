import os
import sys
import logging
from shutil import copyfile, rmtree
import pkg_resources

from . import build
from . import utils
from .recipe import Recipe


def return_hello():
    """ This is a test function for our unittest setup and should be removed when we start using the test setup"""
    return "hello"


def setup_logging(debug, output_dir_path):
    if debug:
        debug_filename = "%s/debug.log" % output_dir_path
        logging.basicConfig(filename = debug_filename, level = logging.DEBUG)
        debug_folder = "%s/debug_output_files" % output_dir_path
        os.mkdir(debug_folder)
    else:
        logging.getLogger().disabled = True


def main(name, version, src, sha, bioconda_recipe_path, debug, test_path=None):
    # Create output directory 
    output_dir_path = "./%s" % name
    os.mkdir(output_dir_path)

    # Setup debugging
    setup_logging(debug, output_dir_path)
    
    # Setup variables
    path = "%s/recipes/%s" % (bioconda_recipe_path, name)
    
    try:
        # run conda-build with --build-only flag
        mini_proc_build, recipe = build.mini_iterative_build(name, version, src, sha)
        print("mini_proc_build return code:", mini_proc_build.returncode)
        for line in mini_proc_build.stdout.split("\n"):
            print(line)

        # run conda-build with tests
        mini_proc_test, recipe = build.mini_iterative_test(name, recipe, test_path)
        print("mini_proc_test return code:", mini_proc_test.returncode)
        for line in mini_proc_test.stdout.split("\n"):
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
