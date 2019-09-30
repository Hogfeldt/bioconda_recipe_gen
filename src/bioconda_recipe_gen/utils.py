import urllib.request
import os
import shutil
import tempfile
import hashlib
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
