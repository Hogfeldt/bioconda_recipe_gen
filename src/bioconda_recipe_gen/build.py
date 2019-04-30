import os
import subprocess
import logging
import tempfile
import pkg_resources
import docker
from shutil import rmtree, copy2, copyfile
from copy import deepcopy

from .utils import download_and_unpack_source, copytree
from .recipe import Recipe


def bioconda_utils_build(package_name, bioconda_recipe_path):
    """ Build a bioconda package with bioconda-utils and return the standard output
    
    Args:
        package_name: Name of the package to build
    """
    wd = os.getcwd()
    os.chdir(bioconda_recipe_path)
    cmd = [
        "bioconda-utils",
        "build",
        "recipes/",
        "config.yml",
        "--packages",
        package_name,
    ]
    proc = subprocess.run(cmd, encoding="utf-8", stdout=subprocess.PIPE)
    os.chdir(wd)
    return proc


def bioconda_utils_build_setup(bioconda_recipe_path, name):
    """ Copy build.sh and meta.yaml templates to bioconda-recipes. Return a Recipe object based on the templates. """
    # SETUP
    # Make a new dir in 'bioconda-recipe/recipes'
    path = "%s/recipes/%s" % (bioconda_recipe_path, name)
    os.mkdir(path)
    # Copy recipe to into the new dir
    resource_package = __name__
    resource_path = "/".join(("recipes", "meta.yaml"))
    meta_template = pkg_resources.resource_string(resource_package, resource_path)
    with open("%s/%s" % (path, "meta.yaml"), "wb") as fp:
        fp.write(meta_template)
    resource_path = "/".join(("recipes", "build.sh"))
    build_template = pkg_resources.resource_string(resource_package, resource_path)
    with open("%s/%s" % (path, "build.sh"), "wb") as fp:
        fp.write(build_template)

    return Recipe(path + "/meta.yaml")


def bioconda_utils_iterative_build(bioconda_recipe_path, name):
    """ Try to build a package with bioconda-utils """
    recipe = bioconda_utils_build_setup(bioconda_recipe_path, name)
    # BUILD
    # Do the iterative build
    dependencies = []
    proc = bioconda_utils_build(name, bioconda_recipe_path)

    if proc.returncode != 0:
        # Check for dependencies
        for line in proc.stdout.split("\n"):
            line_norma = line.lower()
            if "missing" in line_norma:
                print(line_norma)
                if "hdf5" in line_norma:
                    recipe.add_requirement("hdf5", "host")
                    dependencies.append("hdf5")

        # after new requirements are added: write new recipe to meta.yaml
        recipe.write_recipe_to_meta_file()
    proc = bioconda_utils_build(name, bioconda_recipe_path)
    return (proc, dependencies)


def mini_build_setup(name, version, src, hashing):
    """ Copy build.sh and meta.yaml templates to cwd. Return a Recipe object based on the templates. """
    path = "./%s" % name
    os.mkdir("%s/output" % path)
    resource_path = "/".join(("recipes", "meta.yaml"))
    meta_template = pkg_resources.resource_string(__name__, resource_path)
    with open("%s/%s" % (path, "meta.yaml"), "wb") as fp:
        fp.write(meta_template)
    resource_path = "/".join(("recipes", "build.sh"))
    build_template = pkg_resources.resource_string(__name__, resource_path)
    with open("%s/%s" % (path, "build.sh"), "wb") as fp:
        fp.write(build_template)
    return Recipe(path + "/meta.yaml", name, version, src, hashing)


def run_conda_build_mini(name, build_only=True):
    """ Run docker run and build the package in a docker mini image"""
    # Setup image
    client = docker.from_env()
    
    # Run docker image
    flag = "--build-only" if build_only else ""
    path = "%s/%s" % (os.getcwd(), name)
    container = client.containers.run(
        "perhogfeldt/conda-build-mini",
        "conda build %s --output-folder /home/output /mnt/recipe " % flag,
        volumes={path: {"bind": "/mnt/recipe", "mode": "ro"}},
        detach=True,
    )
    result = container.wait()
    stdout = container.logs().decode('utf-8')
    container.remove()
    return (result, stdout)


def run_conda_build_mini_test(name):
    """ Call run_mini_build with the build_only parameter as False """
    return run_conda_build_mini(name, False)


def mini_iterative_build(name, version, src, hashing):
    """ Build a bioconda package with a Docker mini image and try to find missing packages,
        return a tupple with the last standard output and a list of found dependencies.
    
    Args:
        src: A link to where the source file can be downloaded
    """

    recipe = mini_build_setup(name, version, src, hashing)
    print("mini setup done")

    c = 0
    new_recipe = deepcopy(recipe)
    return_code = 1
    while return_code != 0:
        result, stdout = run_conda_build_mini(name)

        for line in stdout.split("\n"):
            line_normalized = line.lower()
            print(line)
            if (
                "autoheader: not found" in line_normalized
            ):  # only occures when minimal build.sh for kallisto is used
                debug_message = (
                    "Because 'autoheader: not found' was in the error message"
                )
                new_recipe.add_requirement(
                    "autoconf", "build", debug_message=debug_message
                )
            if "autoreconf: command not found" in line_normalized:
                debug_message = (
                    "Because 'autoreconf: command not found' was in the error message"
                )
                new_recipe.add_requirement(
                    "autoconf", "build", debug_message=debug_message
                )
            if "autoreconf: failed to run aclocal" in line_normalized:
                debug_message = "Because 'autoreconf: failed to run aclocal' was in the error message"
                new_recipe.add_requirement(
                    "automake", "build", debug_message=debug_message
                )
            if "could not find hdf5" in line_normalized:
                debug_message = "Because 'could not find hdf5' was in the error message"
                new_recipe.add_requirement("hdf5", "host", debug_message=debug_message)
        if new_recipe == recipe:
            break
        else:
            recipe = deepcopy(new_recipe)
            recipe.write_recipe_to_meta_file()
        return_code = result['StatusCode']
        c += 1
        print("%s iteration" % c)

        if not logging.getLogger().disabled:
            src = "%s/%s/output" % (os.getcwd(), name)
            dst = "%s/%s/debug_output_files/build_iter%d" % (os.getcwd(), name, c)
            os.mkdir(dst)
            copytree(src, dst)

    return ((result, stdout), recipe)


def add_tests(name, recipe, test_path):
    """ Copy test files from test_path to './name' and add test files to the recipe """
    print("Copying test files")
    path = "./%s" % name
    copytree(test_path, path)
    recipe.add_tests(test_path)
    recipe.write_recipe_to_meta_file()


def mini_iterative_test(name, recipe, test_path):
    print("mini iterative test started")
    if test_path is not None:
        add_tests(name, recipe, test_path)
    result, stdout = run_conda_build_mini_test(name)
    for line in stdout.split("\n"):
        line_normalized = line.lower()
        if "['zlib'] not in reqs/run" in line_normalized:
            recipe.add_requirement("zlib", "run")
    recipe.write_recipe_to_meta_file()

    if not logging.getLogger().disabled:
        src = "%s/%s/output" % (os.getcwd(), name)
        dst = "%s/%s/debug_output_files/test_iter1" % (os.getcwd(), name)
        os.mkdir(dst)
        copytree(src, dst)

    return ((result, stdout), recipe)


def mini_sanity_check(bioconda_recipe_path, name):
    """ Copy build.sh and meta.yaml templates to cwd. Return a Recipe object based on the templates. """
    recipes_pkg_path = "%s/recipes/%s/" % (bioconda_recipe_path, name)
    os.mkdir(recipes_pkg_path)
    current_recipe_path = "%s/%s/" % (os.getcwd(), name)

    for item in os.listdir(current_recipe_path):
        s = os.path.join(current_recipe_path, item)
        d = os.path.join(recipes_pkg_path, item)

        if not os.path.isdir(s):
            copy2(s, d)
        elif item != "output":
            copytree(s, d)

    # Try to build the package
    proc = bioconda_utils_build(name, bioconda_recipe_path)
    for line in proc.stdout.split("\n"):
        print(line)
    if proc.returncode == 0:
        return True
    else:
        return False
