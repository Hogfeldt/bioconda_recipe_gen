import os
import subprocess
import tempfile
import pkg_resources
from shutil import rmtree

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


def mini_build_setup(name):
    """ Copy build.sh and meta.yaml templates to cwd. Return a Recipe object based on the templates. """
    path = "./%s" % name
    os.mkdir(path)
    resource_path = "/".join(("recipes", "meta.yaml"))
    meta_template = pkg_resources.resource_string(__name__, resource_path)
    with open("%s/%s" % (path, "meta.yaml"), "wb") as fp:
        fp.write(meta_template)
    resource_path = "/".join(("recipes", "build.sh"))
    build_template = pkg_resources.resource_string(__name__, resource_path)
    with open("%s/%s" % (path, "build.sh"), "wb") as fp:
        fp.write(build_template)
    return Recipe(path + "/meta.yaml")


def mini_docker_build():
    """ Run docker build, to make sure that the running docker installation has the required and up to date image """
    with tempfile.TemporaryDirectory() as tmpdir:
        resource_path = "/".join(("containers", "Dockerfile"))
        dockerfile = pkg_resources.resource_string(__name__, resource_path)
        with open("%s/%s" % (tmpdir, "Dockerfile"), "wb") as fp:
            fp.write(dockerfile)
        cmd = ["docker", "build", "--tag=mini-buildenv", tmpdir]
        proc = subprocess.run(cmd, encoding="utf-8", stdout=subprocess.PIPE)
        if proc.returncode != 0:
            return False
        else:
            return True


def run_mini_build(name, build_only=True):
    """ Run docker run and build the package in a docker mini image"""
    flag = "--build-only" if build_only else ""
    path = "%s/%s" % (os.getcwd(), name)
    cmd = [
        "docker",
        "run",
        "-v",
        "%s:/home" % path,
        "--rm",
        "-ti",
        "mini-buildenv",
        "/bin/sh",
        "-c",
        "conda build %s /home" % flag,
    ]
    return subprocess.run(cmd, encoding="utf-8", stdout=subprocess.PIPE)


def run_mini_test(name):
    """ Call run_mini_build with the build_only parameter as False """
    return run_mini_build(name, False)


def mini_iterative_build(name):
    """ Build a bioconda package with a Docker mini image and try to find missing packages,
        return a tupple with the last standard output and a list of found dependencies.
    
    Args:
        src: A link to where the source file can be downloaded
    """

    mini_docker_build()
    print("build done")
    recipe = mini_build_setup(name)
    print("mini setup done")

    # TODO: find a better stop condition
    c = 0
    while c != 5:
        proc = run_mini_build(name)
        for line in proc.stdout.split("\n"):
            line_normalized = line.lower()
            print(line)
            if (
                "autoheader: not found" in line_normalized
            ):  # only occures when minimal build.sh for kallisto is used
                recipe.add_requirement("autoconf", "build")
            if "autoreconf: command not found" in line_normalized:
                recipe.add_requirement("autoconf", "build")
            if "autoreconf: failed to run aclocal" in line_normalized:
                recipe.add_requirement("automake", "build")
            if "could not find hdf5" in line_normalized:
                recipe.add_requirement("hdf5", "host")
                recipe.add_requirement("hdf5", "run") 
        recipe.write_recipe_to_meta_file()
        c += 1
        print("%s iteration" % c)
    proc = run_mini_build(name)
    return (proc, recipe)


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
    proc = run_mini_test(name)
    if "['zlib'] not in reqs/run" in line_normalized:
        recipe.add_requirement("zlib", "run")
    recipe.write_recipe_to_meta_file()
    return (proc, recipe)


def mini_sanity_check(bioconda_recipe_path, name):
    """ Copy build.sh and meta.yaml templates to cwd. Return a Recipe object based on the templates. """
    recipes_kallisto_path = "%s/recipes/%s/" % (bioconda_recipe_path, name)
    os.mkdir(recipes_kallisto_path)
    current_recipe_path = "%s/%s/" % (os.getcwd(), name)

    # Copy meta.yaml and build.sh into bioconda-recipes/recipes/name_of_pkg
    with open(current_recipe_path + "meta.yaml", "r") as f:
        curr_meta = f.read()
    with open(recipes_kallisto_path + "meta.yaml", "w") as f:
        f.write(curr_meta)

    with open(current_recipe_path + "build.sh", "r") as f:
        curr_build = f.read()
    with open(recipes_kallisto_path + "build.sh", "w") as f:
        f.write(curr_build)

    # Try to build the package
    proc = bioconda_utils_build(name, bioconda_recipe_path)
    if proc.returncode == 0:
        return True
    else:
        return False
