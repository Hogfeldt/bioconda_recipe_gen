import argparse
import os
import sys
import logging

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
    parser.add_argument(
        "-n",
        "--name",
        help="Name of your package",
        required=True,
    )
    parser.add_argument(
        "-u",
        "--url",
        help="Url to where the source code of project can be downloaded",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--sha",
        help="The SHA that matches the project which the url argument points to",
        required=True,
    )
    parser.add_argument(
        "-v",
        "--version",
        help="The version number of the build",
        required=True,
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="Set this flag if you want to activate the debug mode. This creates an debug.log file that contains all debug prints",
        action='store_true',
    )
    args = parser.parse_args()

    if bioconda_recipes_exists(args.bioconda_recipe_path):
        if args.tests is None:
            main(args.name, args.version, args.url, args.sha, args.bioconda_recipe_path, args.debug)
        else:
            main(args.name, args.version, args.url, args.sha, args.bioconda_recipe_path, args.debug, args.tests[0])
    else:
        sys.exit("ERROR: Wrong path to bioconda-recipes")
