import urllib.request
import subprocess
import os
import pkg_resources
import shutil
import tempfile
import hashlib


def calculate_md5_checksum(url):
    """ Calculate the md5 checksum of the file found at the url """
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = "%s/file_to_check" % tmpdir
        urllib.request.urlretrieve(url, file_path)
        md5_hash = hashlib.md5(open(file_path, "rb").read()).hexdigest()
    return md5_hash


def copytree(src, dst, symlinks=False, ignore=None):
    """ Enhanced shutil.copytree function. This function will if the destination directory already exists copy all items from source to the destination, instead of throwing a FileExistsError """
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
