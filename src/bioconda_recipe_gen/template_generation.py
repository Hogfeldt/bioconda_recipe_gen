import os
import tempfile
from shutil import rmtree
import validators
import requests

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


def ask_user_for_url():
    url = input("Url to download the code: ")
    while not validators.url(url):
        print("{} is not a valid url. Please try again.".format(url))
        url = input("Url to download the code: ")
    return url


def check_url(url):
    try:
        req = requests.get(url)
    except requests.exceptions.RequestException as error: 
        return "Could not connect to url. Check if the url is correct and try again."
    return str(req.status_code)


def get_url():
    url = ask_user_for_url()    
    res = check_url(url)
    while res != "200":
        print("Error:", res)
        url = ask_user_for_url()
        res = check_url(url)
    return url

def get_user_input():
    name = input("Package name: ")
    version = input("Version: ")
    url = get_url()
    print("Choose the strategy that you use to run your code")
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

