import sys
import urllib.request
import os
import shutil
import tempfile
import hashlib
import tarfile
import zipfile
from bioconda_utils import recipe


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


def get_pkg_build_number(pkg_name, bioconda_recipe_path):
    """ Returns the build number of an exisitng package in the bioconda-recipe/recipes folder """
    recipes_path = "%s/recipes" % bioconda_recipe_path
    meta_yaml_path = "%s/%s" % (recipes_path, pkg_name)
    try:
        cur_recipe = recipe.Recipe.from_file(recipes_path, meta_yaml_path)
        build_number = int(cur_recipe.get("build/number"))
    except:
        build_number = 0
    return build_number


def download_and_unpack_source(src, dir_path):
    """ Download a source file and unpack it """
    try:
        # .tar
        if src.lower().endswith(".tar"):
            urllib.request.urlretrieve(src, "%s/source.tar" % dir_path)
            os.mkdir("%s/source" % dir_path)
            with tarfile.open("%s/source.tar" % dir_path) as tar_ref:
                tar_ref.extractall("%s/source" % dir_path)
        # .tar.gz
        if src.lower().endswith(".tar.gz"):
            urllib.request.urlretrieve(src, "%s/source.tar.gz" % dir_path)
            os.mkdir("%s/source" % dir_path)
            with tarfile.open("%s/source.tar.gz" % dir_path, "r:gz") as tar_ref:
                tar_ref.extractall("%s/source" % dir_path)
        # .tar.bz2
        elif src.lower().endswith(".tar.bz2"):
            urllib.request.urlretrieve(src, "%s/source.tar.bz2" % dir_path)
            os.mkdir("%s/source" % dir_path)
            with tarfile.open("%s/source.tar.bz2" % dir_path, "r:bz2") as tar_ref:
                tar_ref.extractall("%s/source" % dir_path)
        # .tgz
        elif src.lower().endswith(".tgz"):
            urllib.request.urlretrieve(src, "%s/source.tgz" % dir_path)
            os.mkdir("%s/source" % dir_path)
            with tarfile.open("%s/source.tgz" % dir_path, "r:gz") as tar_ref:
                tar_ref.extractall("%s/source" % dir_path)
        # .zip
        elif src.lower().endswith(".zip"):
            urllib.request.urlretrieve(src, "%s/source.zip" % dir_path)
            os.mkdir("%s/source" % dir_path)
            with zipfile.ZipFile("%s/source.zip" % dir_path, "r") as zip_ref:
                zip_ref.extractall("%s/source" % dir_path)
        else:
            print("Unknown fileformat! Cannot unpack %s" % src)
    except urllib.error.HTTPError as e:
        print('HTTP error code: ', e.code)
        print(src)
    except urllib.error.URLError as e:
        print('URL error Reason: ', e.reason)
        print(src)
    except tarfile.ReadError:
        print('Tarfile ReadError')
        print(src)
    except:
        print("Unexpected error:", sys.exc_info()[0])


def is_file_in_folder(filename, folder_path):
    """ Returns True if file is somewhere in the folder. Else False"""
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            if "configure" in f:
                print(f)
            if f == filename:
                return True
    return False