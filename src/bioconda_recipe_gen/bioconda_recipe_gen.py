import os
import sys
import argsparse
from shutil import copyfile, rmtree

from . import build
from . recipe import Recipe


def return_hello():
    """ This is a test function for our unittest setup and should be removed when we start using the test setup"""
    return "hello"


def main():
    parser = argparse.ArgumentParser(description='bioconda-recipe-gen is a tool for automatically generating a bioconda recipe for a given pice of software')
    parser.add_argument('bioconda_recipe_path', help='Path to your local copy of the bioconda-recipe repository')
    args = parser.parse_args()
    bioconda_recipe_path = args.bioconda_recipe_path

    # Setup variables
    name = "kallisto2"
    src = "https://github.com/pachterlab/kallisto/archive/v0.45.0.tar.gz"
    path = "%s/%s" % (bioconda_recipe_path, name)

    project_root = os.path.realpath(__file__).replace(
        "/src/bioconda_recipe_gen/bioconda_recipe_gen.py", ""
    )
    os.chdir(project_root)

    os.mkdir(path)

    # Copy recipe to into Bioconda
    copyfile("src/bioconda_recipe_gen/recipes/meta.yaml", path + "/meta.yaml")
    copyfile("src/bioconda_recipe_gen/recipes/build.sh", path + "/build.sh")

    recipe = Recipe(path + "/meta.yaml")

    proc = build.bioconda_utils_build(name)
    for line in proc.stdout.split("\n"):
        print(line)
    print("return code: " + str(proc.returncode) + "\n")
    if proc.returncode != 0:
        # Check for dependencies
        for line in proc.stdout.split("\n"):
            line_norma = line.lower()
            if "missing" in line_norma:
                print(line_norma)
                if "hdf5" in line_norma:
                    recipe.add_requirement("hdf5", "host")

        # after new requirements are added: write new recipe to meta.yaml
        recipe.write_recipe_to_meta_file()
    else:
        print("Build succeded")
        sys.exit(0)

    # TODO: Try to build with with alpine image
    proc = build.alpine_build(src)
    for line in proc.stdout.split("\n"):
        print(line)

    proc = build.bioconda_utils_build(name)
    for line in proc.stdout.split("\n"):
        print(line)

    # clean up
    rmtree(path)


if __name__ == "__main__":
    main()
