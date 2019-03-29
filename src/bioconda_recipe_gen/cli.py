import argparse

from .bioconda_recipe_gen import main

def start():
    parser = argparse.ArgumentParser(description='bioconda-recipe-gen is a tool for automatically generating a bioconda recipe for a given pice of software')
    parser.add_argument('bioconda_recipe_path', help='Path to your local copy of the bioconda-recipe repository')
    args = parser.parse_args()

    main(args.bioconda_recipe_path)
