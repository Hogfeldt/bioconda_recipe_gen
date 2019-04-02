import urllib.request
import subprocess
import os

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
