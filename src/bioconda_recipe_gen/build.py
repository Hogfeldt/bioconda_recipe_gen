import os
import subprocess
import tempfile

from .utils import download_and_unpack_source

DOCKERFILE_TEMPLATE = """
FROM alpine:3.7

RUN echo http://dl.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories
#RUN echo http://dl.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories

RUN apk add --update \
    bash \
    g++ \
    gcc \
    cmake \
    make

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


def alpine_docker_build(tmpdir, dockerfile):
    """ Run docker build, to make sure the running docker installation has the requires and up to date image """
    with open("%s/Dockerfile" % tmpdir, "w") as fp:
        fp.write("%s\nCOPY ./source /package" % dockerfile)
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
    dependencies = []
    with tempfile.TemporaryDirectory() as tmpdir:
        download_and_unpack_source(src, tmpdir)
        # look for hdf5
        alpine_docker_build(tmpdir, dockerfile)
        proc = run_alpine_build()
        for line in proc.stdout.split("\n"):
            line_normalized = line.lower()
            if "missing" in line_normalized:
                dockerfile += "\nRUN apk add --update \ \n    hdf5"
                dependencies.append('hdf5')
        # look for zlib
        alpine_docker_build(tmpdir, dockerfile)
        proc = run_alpine_build()
        for line in proc.stdout.split("\n"):
            line_normalized = line.lower()
            if "missing" in line_normalized:
                dockerfile += "\nRUN apk add --update \ \n    zlib-dev"
                dependencies.append('zlib-dev')
        # look for autoconf when running make install
        alpine_docker_build(tmpdir, dockerfile)
        proc = run_alpine_build()
        std_out = proc.stdout.lower()
        if "make install failed" in std_out and "autoheader: not found" in std_out:
            dockerfile += "\nRUN apk add --update \ \n    autoconf"
            dependencies.append('autoconf')
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
                dependencies.remove('hdf5')
                dependencies.append('hdf5-dev')
        alpine_docker_build(tmpdir, dockerfile)
        proc = run_alpine_build()
    return (proc, dependencies)
