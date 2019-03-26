import os
import subprocess
import tempfile
import urllib.request

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


def alpine_docker_build(tmpdir):
    """ Run docker build, to make sure the running docker installation has the requires and up to date image """
    with open("%s/Dockerfile" % tmpdir, "w") as fp:
        print('%s\nCOPY ./source /package' % DOCKERFILE_TEMPLATE)
        fp.write('%s\nCOPY ./source /package' % DOCKERFILE_TEMPLATE)
    cmd = ["docker", "build", "--tag=alpine-buildenv", tmpdir]
    proc = subprocess.run(cmd, encoding="utf-8", stdout=subprocess.PIPE)
    if proc.returncode != 0:
        return False
    else:
        return True


# TODO: this function should probably be moved to some kind of utils file
def download_and_unpack_source(src, dir_path):
    if src.split(".")[-2] == "tar" and src.split(".")[-1] == "gz":
        # TODO: Handle exceptions
        urllib.request.urlretrieve(src, "%s/source.tar.gz" % dir_path)
        os.mkdir("%s/source" % dir_path)
        cmd = [
            "tar",
            "-xzf",
            "%s/source.tar.gz" % dir_path,
            "-C",
            "%s/source" % dir_path,
            "--strip-components=1",
        ]
        subprocess.run(cmd, encoding="utf-8", stdout=subprocess.PIPE)


def run_alpine_build():
    cmd = [
        "docker",
        "run",
        "--rm",
        "-ti",
        "alpine-buildenv",
        "/bin/sh",
        "-c",
        "mkdir build; cd build; cmake ..; make .",
    ]
    proc = subprocess.run(cmd, encoding="utf-8", stdout=subprocess.PIPE)
    for line in proc.stdout.split('\n'):
        print(line)
    return proc

def alpine_build(src):
    """ Build a bioconda package with an Alpine Docker image and return the standard output 
    
    Args:
        src: A link to where the source file can be downloaded
    """
    # build alpine image
    with tempfile.TemporaryDirectory() as tmpdir:
        download_and_unpack_source(src, tmpdir)
        alpine_docker_build(tmpdir)
        proc = run_alpine_build()
    return proc
