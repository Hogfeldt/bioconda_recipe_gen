import argparse
import os
import sys
import logging

from .bioconda_recipe_gen import main
from .preprocessors.from_args import preprocess as args_preprocess
from .preprocessors.from_files import preprocess as files_preprocess


def bioconda_recipes_exists(path):
    return os.path.exists("%s/recipes" % path) and os.path.exists(
        "%s/config.yml" % path
    )

def call_main(args, recipes, build_scripts):
    if bioconda_recipes_exists(args.bioconda_recipe_path):
        main(args.bioconda_recipe_path, recipes, build_scripts, args.debug)
    else:
        sys.exit("ERROR: Wrong path to bioconda-recipes")

def recipe_by_files_handler(args):
    recipes, build_scripts = files_preprocess(args)
    call_main(args, recipes, build_scripts)


def recipe_by_args_handler(args):
    recipes, build_scripts = args_preprocess(args)
    call_main(args, recipes, build_scripts)


def start():
    # Top-level Parser
    parser = argparse.ArgumentParser(
        prog="bioconda-recipe-gen",
        description="bioconda-recipe-gen is a tool for automatically generating a bioconda recipe for a given pice of software",
    )
    parser.add_argument(
        "bioconda_recipe_path",
        help="Path to your local copy of the bioconda-recipe repository",
    )
    subparser = parser.add_subparsers(
        help="Choose how you would like to give informations about the package"
    )

    # Subparser: Give recipe from arguments
    parser_args = subparser.add_parser(
        "from-args", help="Add recipe information through cli agruments"
    )
    parser_args.add_argument(
        "--tests",
        help="Add path to a directory, containing tests for your package. The Directory will have to contain a run_test.[py,pl,sh,bat] file and eventually other files needed for the run_test.[py,pl,sh,bat] file",
        nargs=1,
    )
    parser_args.add_argument(
        "--files",
        "--test-files",
        help="Add a list of test files that should be added to the recipe. This is just an alternative way to the same as the --tests flags",
        nargs="*",
    )
    parser_args.add_argument(
        "--patches",
        help="Add paths to folder with the patch files that should be used for the project",
    )
    parser_args.add_argument(
        "--commands", "--test-commands", help="Add test command to recipe", nargs="*"
    )
    parser_args.add_argument(
        "-d",
        "--debug",
        help="Set this flag if you want to activate the debug mode. This creates an debug.log file that contains all debug prints",
        action="store_true",
    )
    parser_args.add_argument("-n", "--name", help="Name of your package", required=True)
    parser_args.add_argument(
        "-u",
        "--url",
        help="Url to where the source code of project can be downloaded",
        required=True,
    )
    parser_args.add_argument(
        "-v", "--version", help="The version number of the build", required=True
    )
    parser_args.add_argument(
        "--cmake",
        "--cmake-flags",
        help="If you don't want to run cmake with our default flags: 'DCMAKE_INSTALL_PREFIX=$PREFIX' and ' DINSTALL_PREFIX=$PREFIX', you can add your own here. Note: do NOT added the dashes in front of the flags.",
        nargs="*",
    )
    # make sure that we either SHA or MD5 (not both of them, not none of them)
    group = parser_args.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-s",
        "--sha",
        help="The SHA that matches the project which the url argument points to",
    )
    group.add_argument(
        "-m",
        "--md5",
        help="The MD5 that matches the project which the url argument points to",
    )
    parser_args.set_defaults(func=recipe_by_args_handler)

    # Subparser: Give a path to a build.sh and a meta.yaml
    parser_files = subparser.add_parser(
        "from-files", help="Add recipe informations from build.sh and meta.yaml"
    )
    parser_files.add_argument("recipe_path", help="Path to build.sh and meta.yaml")
    parser_files.add_argument(
        "-d",
        "--debug",
        help="Set this flag if you want to activate the debug mode. This creates an debug.log file that contains all debug prints",
        action="store_true",
    )
    parser_files.set_defaults(func=recipe_by_files_handler)

    # Evaluate the parsed arguments
    args = parser.parse_args()
    args.func(args)
