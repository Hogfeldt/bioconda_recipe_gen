import os
import subprocess
import tempfile
import pkg_resources

from .utils import download_and_unpack_source
from .recipe import Recipe

DOCKERFILE_TEMPLATE = """
FROM alpine:3.7

RUN echo http://dl.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories
#RUN echo http://dl.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories

RUN apk add --update \
    bash \

WORKDIR /package
"""


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


def alpine_docker_build(tmpdir, dockerfile, exstras=""):
    """ Run docker build, to make sure the running docker installation has the requires and up to date image """
    with open("%s/Dockerfile" % tmpdir, "w") as fp:
        fp.write("%s\nCOPY ./source /package %s" % (dockerfile, exstras))
    cmd = ["docker", "build", "--tag=alpine-buildenv", tmpdir]
    proc = subprocess.run(cmd, encoding="utf-8", stdout=subprocess.PIPE)
    if proc.returncode != 0:
        return False
    else:
        return True


def run_alpine_build():
    """ Run docker run and build the package in a docker Alpine image"""
    cmd = [
        "docker",
        "run",
        "--rm",
        "-ti",
        "alpine-buildenv",
        "/bin/sh",
        "-c",
        "mkdir build; cd build; cmake .. && echo 'cmake pass' || echo 'cmake failed'; make . && echo 'make pass' || echo 'make failed'; make install && echo 'make install pass' || echo 'make install failed'",
    ]
    return subprocess.run(cmd, encoding="utf-8", stdout=subprocess.PIPE)


def alpine_build(src):
    """ Build a bioconda package with an Alpine Docker image and return the standard output 
    
    Args:
        src: A link to where the source file can be downloaded
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        download_and_unpack_source(src, tmpdir)
        alpine_docker_build(tmpdir, DOCKERFILE_TEMPLATE)
        proc = run_alpine_build()
    return proc


def alpine_iterative_build(src):
    """ Build a bioconda package with an Alpine Docker image and try to find missing packages,
        return a tupple with the last standard output and a list of found dependencies.
    
    Args:
        src: A link to where the source file can be downloaded
    """
    dockerfile = DOCKERFILE_TEMPLATE
    dependencies = ["g++", "gcc", "make", "cmake"]
    for d in dependencies:
        dockerfile += "\nRUN apk add --update \ \n    %s" % d

    with tempfile.TemporaryDirectory() as tmpdir:
        download_and_unpack_source(src, tmpdir)
        # look for hdf5
        alpine_docker_build(tmpdir, dockerfile)
        proc = run_alpine_build()
        for line in proc.stdout.split("\n"):
            line_normalized = line.lower()
            if "missing" in line_normalized:
                dockerfile += "\nRUN apk add --update \ \n    hdf5"
                dependencies.append("hdf5")
        # look for zlib
        alpine_docker_build(tmpdir, dockerfile)
        proc = run_alpine_build()
        for line in proc.stdout.split("\n"):
            line_normalized = line.lower()
            if "missing" in line_normalized:
                dockerfile += "\nRUN apk add --update \ \n    zlib-dev"
                dependencies.append("zlib-dev")
        # look for autoconf when running make install
        alpine_docker_build(tmpdir, dockerfile)
        proc = run_alpine_build()
        std_out = proc.stdout.lower()
        if "make install failed" in std_out and "autoheader: not found" in std_out:
            dockerfile += "\nRUN apk add --update \ \n    autoconf"
            dependencies.append("autoconf")
        # look for hdf5-dev when running make install
        alpine_docker_build(tmpdir, dockerfile)
        proc = run_alpine_build()
        std_out = proc.stdout.lower()
        if (
            "make install failed" in std_out
            and "hdf5.h: no such file or directory" in std_out
        ):
            if "hdf5" in dockerfile:
                dockerfile = dockerfile.replace("hdf5", "hdf5-dev")
                dependencies.remove("hdf5")
                dependencies.append("hdf5-dev")
        alpine_docker_build(tmpdir, dockerfile)
        proc = run_alpine_build()
    
    return (proc, dependencies)


def run_alpine_test(test, deps_to_remove):
    """ Run docker run and and try the test command """
    rm_cmd = "apk del "
    for d in deps_to_remove:
        rm_cmd += "%s " % d
    cmd = [
        "docker",
        "run",
        "--rm",
        "-ti",
        "alpine-buildenv",
        "/bin/sh",
        "-c",
        "%s;%s && echo 'test pass' || echo 'test failed'" % (rm_cmd, test),
    ]
    return subprocess.run(cmd, encoding="utf-8", stdout=subprocess.PIPE)


def alpine_run_test(src, build_dependencies, test):
    dockerfile = DOCKERFILE_TEMPLATE
    dependencies = ["g++", "gcc"]
    deps_to_remove = [d for d in build_dependencies if d != "gcc" and d != "g++"]
    docker_exstra = "\nRUN mkdir build; cd build; cmake ..; make .; make install;"
    for d in build_dependencies:
        dockerfile += "\nRUN apk add --update \ \n    %s" % d
    with tempfile.TemporaryDirectory() as tmpdir:
        download_and_unpack_source(src, tmpdir)
        # Look for missing hdf5
        alpine_docker_build(tmpdir, dockerfile, docker_exstra)
        proc = run_alpine_test(test, deps_to_remove)
        if "libhdf5.so" in proc.stdout:
            docker_exstra += "\nRUN apk add --update hdf5"
            dependencies.append("hdf5")
        alpine_docker_build(tmpdir, dockerfile, docker_exstra)
        proc = run_alpine_test(test, deps_to_remove)
        if "test pass" in proc.stdout:
            return (True, dependencies)
        else:
            return (False, dependencies)
