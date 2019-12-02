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
        file_path = os.path.join(tmpdir, "file_to_check")
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
    recipes_path = os.path.join(bioconda_recipe_path, "recipes")
    meta_yaml_path = os.path.join(recipes_path, pkg_name)
    try:
        cur_recipe = recipe.Recipe.from_file(recipes_path, meta_yaml_path)
        build_number = int(cur_recipe.get("build/number"))
    except:
        build_number = 0
    return build_number


def download_and_unpack_source(src, dir_path):
    """ Download a source file and unpack it """
    unpack_path = os.path.join(dir_path, "source")
    os.mkdir(unpack_path)
    try:
        # .tar
        if src.lower().endswith(".tar"):
            archive_path = os.path.join(dir_path, "source.tar")
            urllib.request.urlretrieve(src, archive_path)
            with tarfile.open(archive_path) as tar_ref:
                tar_ref.extractall(unpack_path)
        # .tar.gz
        if src.lower().endswith(".tar.gz"):
            archive_path = os.path.join(dir_path, "source.tar.gz")
            urllib.request.urlretrieve(src, archive_path)
            with tarfile.open(archive_path, "r:gz") as tar_ref:
                tar_ref.extractall(unpack_path)
        # .tar.bz2
        elif src.lower().endswith(".tar.bz2"):
            archive_path = os.path.join(dir_path, "source.tar.bz2")
            urllib.request.urlretrieve(src, archive_path)
            with tarfile.open(archive_path, "r:bz2") as tar_ref:
                tar_ref.extractall(unpack_path)
        # .tgz
        elif src.lower().endswith(".tgz"):
            archive_path = os.path.join(dir_path, "source.tgz")
            urllib.request.urlretrieve(src, archive_path)
            with tarfile.open(archive_path, "r:gz") as tar_ref:
                tar_ref.extractall(unpack_path)
        # .zip
        elif src.lower().endswith(".zip"):
            archive_path = os.path.join(dir_path, "source.zip")
            urllib.request.urlretrieve(src, archive_path)
            with zipfile.ZipFile(archive_path, "r") as zip_ref:
                zip_ref.extractall(unpack_path)
        else:
            print("Unknown fileformat! Cannot unpack %s" % src)
            return None
    except urllib.error.HTTPError as e:
        print("HTTP error code: ", e.code)
        print(src)
    except urllib.error.URLError as e:
        print("URL error Reason: ", e.reason)
        print(src)
    except tarfile.ReadError:
        print("Tarfile ReadError")
        print(src)
    except:
        print("Unexpected error:", sys.exc_info()[0])
    return unpack_path


def is_file_in_folder(filename, folder_path):
    """ Returns True if file is in the folder (not checking subfolders). Else False"""
    for f in os.listdir(folder_path):
        if f == filename:
            return True
    return False
