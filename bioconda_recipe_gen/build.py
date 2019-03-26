import os
import subprocess

def bioconda_utils_build(package_name):
    ''' Build a bioconda package and return the standard output
    
    Args:
        package_name: Name of the package to build
    '''
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

def alpine_build():
    pass
