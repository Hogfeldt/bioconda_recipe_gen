import os
import tempfile
from shutil import rmtree

from .buildscript import BuildScript
from .filesystem import Filesystem
from .utils import calculate_md5_checksum, download_and_unpack_source
from .recipe import Recipe


def get_strategy():
    strategies = ["cmake", "python2", "python3"]
    strategy = input("{}: ".format(strategies))
    while strategy not in strategies:
        print("{} is not one of the options. Choose between: {}".format(strategy, strategies))
        strategy = input("{}: ".format(strategies))
    return strategy


def get_user_input():
    name = input("Package name: ")
    version = input("Version: ")
    url = input("Url to download the code: ")
    print("Choose the ? that you use to run your code")
    strategy = get_strategy()
    return name, version, url, strategy


def make_recipe(name, version, url, path, strategy):
    recipe = Recipe(name, version, path, strategy)
    recipe.add_source_url(url)
    recipe.add_build_number(0)
    recipe.add_checksum_md5(calculate_md5_checksum(url))
    return recipe


def make_buildscript(name, url, path, strategy):
    with tempfile.TemporaryDirectory() as tmpdir:
        download_and_unpack_source(url, tmpdir)
        source_path = os.path.join(tmpdir, "source")
        source_code_path = os.path.join(source_path, os.listdir(source_path)[0])
        filesystem = Filesystem(source_code_path)
    build_script = BuildScript(name, path, strategy, filesystem)
    return build_script


def create_path(name):
    path = os.path.join(os.getcwd(), name)
    if os.path.exists(path):
        rmtree(path)
    os.mkdir(path)
    return path


def init(args):
    name, version, url, strategy = get_user_input()
    path = create_path(name)
    recipe = make_recipe(name, version, url, path, strategy)
    build_script = make_buildscript(name, url, path, strategy)

    recipe.write_recipe_to_meta_file()
    build_script.write_build_script_to_file()

