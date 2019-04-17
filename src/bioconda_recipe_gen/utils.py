import urllib.request
import subprocess
import os
import pkg_resources
import shutil

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def download_and_unpack_source(src, dir_path):
    """ Download a source file and unpack it """
    # TODO: should probably chech with endswith() instead
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

def map_alpine_pkg_to_conda_pkg(alpine_pkg):
    resource_package = __name__
    loaded_map_binary = pkg_resources.resource_string(resource_package, "alpine_to_conda_map.txt")
    loaded_map = loaded_map_binary.decode("utf-8")
    for line in loaded_map.splitlines():
        if line.startswith(alpine_pkg):
            _, conda_pkg = line.split("#")
            return conda_pkg
    return None
