import argparse
import os
import sys

from .bioconda_recipe_gen import main


def bioconda_recipes_exists(path):
    return os.path.exists("%s/recipes" % path) and os.path.exists(
        "%s/config.yml" % path
    )


def start():
    parser = argparse.ArgumentParser(
        description="bioconda-recipe-gen is a tool for automatically generating a bioconda recipe for a given pice of software"
    )
    parser.add_argument(
        "bioconda_recipe_path",
        help="Path to your local copy of the bioconda-recipe repository",
    )
    parser.add_argument(
        "--tests",
        help="Add path to a directory, containing tests for your package. The Directory will have to contain a run_test.[py,pl,sh,bat] file and eventually other files needed for the run_test.[py,pl,sh,bat] file",
        nargs=1,
    )
    args = parser.parse_args()

    if bioconda_recipes_exists(args.bioconda_recipe_path):
        main(args.bioconda_recipe_path, args.tests[0])
    else:
        sys.exit("ERROR: Wrong path to bioconda-recipes")
