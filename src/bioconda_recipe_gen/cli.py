import argparse
import os
import sys
import logging
from shutil import rmtree

from .bioconda_recipe_gen import main
from .preprocessors.from_args import preprocess as args_preprocess
from .preprocessors.from_files import preprocess as files_preprocess
from .preprocessors.sdist_optimization import sdist_optimization


def bioconda_recipes_exists(path):
    recipes_path = os.path.join(path, "recipes")
    config_path = os.path.join(path, "config.yml")
    return os.path.exists(recipes_path) and os.path.exists(config_path)


def call_main(args, recipes, build_scripts):
    if bioconda_recipes_exists(args.bioconda_recipe_path):
        main(args.bioconda_recipe_path, recipes, build_scripts, args.debug)
    else:
        sys.exit("ERROR: Wrong path to bioconda-recipes")


def recipe_by_files_handler(args):
    recipes, build_scripts = files_preprocess(args)
    if args.strategy == "python3" or args.strategy == "python2":
        for recipe in recipes:
            sdist_optimization(recipe)
    call_main(args, recipes, build_scripts)


def recipe_by_args_handler(args):
    recipes, build_scripts = args_preprocess(args)
    call_main(args, recipes, build_scripts)


def setup_logging(debug, output_dir_path):
    if debug:
        debug_filename = os.path.join(output_dir_path, "debug.log")
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(filename=debug_filename, filemode="w", level=logging.DEBUG)
        debug_folder = os.path.join(output_dir_path, "debug_output_files")
        if os.path.exists(debug_folder):
            rmtree(debug_folder)
        os.mkdir(debug_folder)
    else:
        logging.getLogger().disabled = True


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
    parser_args.add_argument(
        "-t",
        "--template",
        help="Specify the template that should be used for the build.sh file",
        required=True,
        choices=['cmake', 'python'],
    )
    parser_args.add_argument(
        "--imports",
        "--command-imports",
        help="Add a list of packages that should be added to the test/imports segments",
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
    parser_files.add_argument(
        "--strategy",
        help="The strategy that should be used",
        choices=["cmake", "autoconf", "python2", "python3"],
        required=True,
    )
    parser_files.set_defaults(func=recipe_by_files_handler)

    # Evaluate the parsed arguments
    args = parser.parse_args()

    # Setup debugging
    if hasattr(args, "recipe_path"):
        setup_logging(args.debug, args.recipe_path)
    else:
        recipe_path = os.path.join(os.getcwd(), args.name)
        print("recipe_path", recipe_path)
        args.recipe_path = recipe_path
        setup_logging(args.debug, recipe_path)

    # Call specified function
    args.func(args)
