import os
import subprocess
import tempfile

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


def bioconda_utils_build(package_name):
    """ Build a bioconda package with bioconda-utils and return the standard output
    
    Args:
        package_name: Name of the package to build
    """
    wd = os.getcwd()
    os.chdir("../bioconda-recipes")
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


def alpine_docker_build():
    """ Run docker build, to make sure the running docker installation has the requires and up to date image """
    with tempfile.TemporaryDirectory() as tmpdir:
        with open('%s/Dockerfile' % tmpdir, 'w') as fp:
            fp.write(DOCKERFILE_TEMPLATE)
        cmd = [
            "docker",
            "build",
            "--tag=alpine-buildenv",
            tmpdir,
        ]
        proc = subprocess.run(cmd, encoding="utf-8", stdout=subprocess.PIPE)
    if proc.returncode != 0:
        return False
    else:
        return True


def alpine_build():
    """ Build a bioconda package with an Alpine Docker image and return the standard output 
    
    Args:

    """
    # build alpine image
    if alpine_docker_build():
        # on succesfull build: Download the source and unpack
    # Run the alpine image with acces to the source files
    # make build directory
    # run $cmake ..
    # if succesfull
    # run $make .
    pass
