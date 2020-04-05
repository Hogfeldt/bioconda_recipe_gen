import os
import sys
import logging
from shutil import copyfile, rmtree
from git import Repo

from . import build

BIOCONDA_RECIPES = 'https://github.com/birgorg/bioconda-recipes'

def main(bioconda_recipe_path, recipes, build_scripts, debug):
    success = False
    while not success and build_scripts:
        recipe = recipes.pop(0)
        build_script = build_scripts.pop(0)

        if os.path.exists(recipe.path):
            # prepare for new build phase
            output_dir = os.path.join(recipe.path, "output")
            if os.path.exists(output_dir):
                rmtree(output_dir)

        # run conda-build with --build-only flag
        mini_proc_build, recipe, build_script = build.mini_iterative_build(
            recipe, build_script
        )
        print("mini_proc_build return code:", mini_proc_build[0]["StatusCode"])
        for line in mini_proc_build[1].split("\n"):
            print(line)

        # run conda-build with tests
        mini_proc_test, recipe = build.mini_iterative_test(recipe, build_script)
        print("mini_proc_test return code:", mini_proc_test[0]["StatusCode"])
        for line in mini_proc_test[1].split("\n"):
            print(line)

        # Sanity check
        success = build.mini_sanity_check(bioconda_recipe_path, recipe)

        # copy the final recipe into the current directory
        copyfile(
            os.path.join(recipe.path, "meta.yaml"),
            os.path.join(os.getcwd(), "meta.yaml"),
        )

    if success:
        print("SUCCESS: Package was successfully build")
        sys.exit(0)
    else:
        print("ERROR: Didn't pass the sanity check!")
        sys.exit(1)
