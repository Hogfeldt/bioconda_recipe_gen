import os
import subprocess

def bioconda_utils_build(name, wd):
    os.chdir("../bioconda-recipes")
    cmd = [
        "bioconda-utils",
        "build",
        "recipes/",
        "config.yml",
        "--packages",
        "kallisto2",
    ]
    proc = subprocess.run(cmd, encoding="utf-8", stdout=subprocess.PIPE)

    os.chdir(wd)
    return proc
