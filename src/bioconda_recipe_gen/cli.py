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
    args = parser.parse_args()

    if bioconda_recipes_exists(args.bioconda_recipe_path):
        main(args.bioconda_recipe_path)
    else:
        sys.exit("ERROR: Wrong path to bioconda-recipes")
