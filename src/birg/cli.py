import argparse
import os
import sys
import logging
from shutil import rmtree
from tempfile import TemporaryDirectory
from git import Repo

from .birg import main
from .preprocessors.from_files import preprocess as files_preprocess
from .preprocessors.sdist_optimization import sdist_optimization
from .template_generation import init

BIOCONDA_RECIPES = 'https://github.com/birgorg/bioconda-recipes'

def build(args):
    with TemporaryDirectory() as bioconda_recipe_path:
        _ = Repo.clone_from(BIOCONDA_RECIPES, bioconda_recipe_path)
        recipes, build_scripts = files_preprocess(args, bioconda_recipe_path)
        if args.strategy == "python3" or args.strategy == "python2":
            for recipe in recipes:
                sdist_optimization(recipe)
        main(bioconda_recipe_path, recipes, build_scripts, args.debug)

def setup_logging(debug, output_dir_path):
    if debug:
        if not os.path.exists(output_dir_path):
            os.mkdir(output_dir_path)
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
        prog="birg",
        description="Bioconda Recipe Generator is a tool which applies an heuristic approach for automatically generating a bioconda recipe for a given pice of software",
    )
    subparser = parser.add_subparsers(
        help="Which functionality would you like to run: init or build",
        dest='command'
    )

    # Subparser: Run init
    parser_init = subparser.add_parser(
        "init",
        help="Helps create a template that can be used for the 'build' command"
    )
    parser_init.set_defaults(func=init)

    # Subparser: Give a path to a build.sh and a meta.yaml
    parser_files = subparser.add_parser(
        "build",
        help="Build the recipe from the template generate by 'init'"
    )
    parser_files.add_argument(
        "recipe_path",
        help="Path to folder with meta.yaml and build.sh templates",
    )
    parser_files.add_argument(
        "strategy",
        help="The ? that you used when creating the template with 'init'",
        choices=["cmake", "python2", "python3"],
    )
    parser_files.add_argument(
        "-d",
        "--debug",
        help="Set this flag if you want to activate the debug mode. This creates an debug.log file that contains all debug prints",
        action="store_true",
    )
    parser_files.set_defaults(func=build)

    # Evaluate the parsed arguments
    args = parser.parse_args()

    # Setup debugging
    if hasattr(args, "debug"):
        setup_logging(args.debug, args.recipe_path)

    # Call specified function
    args.func(args)
