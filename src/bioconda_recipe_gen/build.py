import hashlib
import os
import io
import tarfile
import subprocess
import logging
import docker
import re
import json
from shutil import rmtree, copy2
from copy import deepcopy
from .utils import copytree, remove_version_from_pkg
from .str_to_pkg import str_to_pkg
from distutils.version import LooseVersion


def bioconda_utils_build(package_name, bioconda_recipe_path):
    """ Build a bioconda package with bioconda-utils and return the standard output. """
    wd = os.getcwd()
    os.chdir(bioconda_recipe_path)
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


def mini_build_setup(recipe, build_script):
    """ Write build.sh and meta.yaml recipe path. """
    recipe.write_recipe_to_meta_file()
    build_script.write_build_script_to_file()
    os.mkdir(os.path.join(recipe.path, "output"))


def run_conda_build_mini(recipe_path, build_only=True):
    """ Run docker run and build the package in a docker mini image"""
    # Setup image
    client = docker.from_env()
    # Run docker image
    flag = "--build-only" if build_only else ""
    try:
        container = client.containers.run(
            "perhogfeldt/conda-build-mini:latest",
            "conda build %s --output-folder /home/output /mnt/recipe -c bioconda -c conda-forge"
            % flag,
            volumes={recipe_path: {"bind": "/mnt/recipe", "mode": "ro"}},
            detach=True,
        )
        result = container.wait()
        stdout = container.logs().decode("utf-8")
        if result["StatusCode"] is 0:
            for line in stdout.split("\n"):
                if "anaconda upload " in line:
                    output_file = line.split()[2]
                    stream, info = container.get_archive(output_file)
                    fd = io.BytesIO()
                    for b in stream:
                        fd.write(b)
                    fd.seek(0)
                    tar_file = tarfile.open(mode="r", fileobj=fd)
                    tar_file.extractall(os.path.join(recipe_path, "output"))
    finally:
        container.remove()
    return (result, stdout)


def run_conda_build_mini_test(recipe_path):
    """ Call run_mini_build with the build_only parameter as False """
    return run_conda_build_mini(recipe_path, False)


def choose_version(pkg_name, version_list, py_version):
    """ Assumes that the input is the list of different dictionaries
    that conda search returns for each pkg it finds.
    Returns the version that the user chooses. """
    # TODO: right now it assumes python packages as this is the
    # only time that we call it, BUT check if there is some way to end up
    # here that would make it crash (e.g. build cmake that makes use of python)
    potential_version = set()
    for entry in version_list:
        if py_version == "python3":
            if "py2" not in entry["build"]:
                potential_version.add(entry["version"])
        else:
            if "py3" not in entry["build"]:
                potential_version.add(entry["version"])
    potential_version = list(potential_version)

    if not potential_version:
        return None

    potential_version = sorted(potential_version, key=LooseVersion, reverse=True)
    # Ask the user
    print("#" * 40)
    print("We found the following potential versions for", pkg_name)
    print("Type y to add without version. Else type the number of the wanted package (applied as >=):")
    for i, ver in enumerate(potential_version):
        print("%d: %s" % (i, ver))
    answer = input()
    # TODO: add some defensive programming here to avoid 'wrong' user input
    if answer == "y":
        return None
    else:
        return potential_version[int(answer)]


def get_correct_pkg_name(pkg_name, extensions, strategy):
    """ Takes a pkg name as input and returns the name of the most
    likely corresponding conda pkg with regard to the 'extension'
    you specify.
    E.g. docker-py is chosen over a packaged called
    docker, if you specify on of the extensions as py.

    The order of the extensions in the list 'extensions' is the
    priority of which they are used (first being highest priority).

    Returns None if no match was found. """
    normalised_pkg_name, _ = remove_version_from_pkg(pkg_name)
    normalised_pkg_name = normalised_pkg_name.replace("-", "*").replace("_", "*").replace(".", "*")
    cmd = ["conda", "search", "*%s*" % normalised_pkg_name, "--json"]
    proc = subprocess.run(cmd, encoding="utf-8", stdout=subprocess.PIPE)
    json_dict = json.loads(proc.stdout)
    best_pkg_match = None
    if len(json_dict) == 1:
        best_pkg_match = list(json_dict.keys())[0]
    elif len(json_dict) > 1:
        normalised_pkg_name = normalised_pkg_name.replace("*", "")
        best_pkg_idx = len(extensions)
        for cur_pkg in json_dict.keys():
            normalised_cur_pkg = cur_pkg.replace("-", "").replace("_", "")
            normalised_pkg_name = normalised_pkg_name.lower()
            extra_content_in_name = normalised_cur_pkg.replace(normalised_pkg_name, "", 1)
            if extra_content_in_name == "" and best_pkg_idx == len(extensions):
                best_pkg_match = cur_pkg
            else:
                for idx, ext in enumerate(extensions):
                    if extra_content_in_name == ext and idx < best_pkg_idx:
                        best_pkg_match = cur_pkg
                        best_pkg_idx = idx
                        if best_pkg_idx == 0:
                            # we found the best case
                            break
    if best_pkg_match is None:
        return None

    version_list = json_dict[best_pkg_match]
    chosen_version = choose_version(best_pkg_match, version_list, strategy)
    if chosen_version is None:
        return best_pkg_match

    best_pkg_match = "%s>=%s" % (best_pkg_match, chosen_version)
    return best_pkg_match


def mini_iterative_build(recipe, build_script):
    """ Build a bioconda package with a Docker mini image and try to find missing packages,
        return a tuple with the last standard output and a list of found dependencies.
    """

    mini_build_setup(recipe, build_script)
    print("mini setup done")
    c = 0
    new_recipe = deepcopy(recipe)
    added_packages = []
    return_code = 1
    while return_code != 0:
        result, stdout = run_conda_build_mini(recipe.path)
        for line in stdout.split("\n"):
            line_normalized = line.lower()
            print(line)

            # Look for python packages
            potential_python_pkg = re.search(
                r"modulenotfounderror: no module named '(.*)'", line_normalized
            )
            if not potential_python_pkg:
                potential_python_pkg = re.search(
                    r"importerror: no module named (.*)", line_normalized
                )
            if not potential_python_pkg:
                potential_python_pkg = re.search(
                    r"cannot find the path for the command `(.*)`", line_normalized
                )
            if potential_python_pkg:
                pkg_name = potential_python_pkg.group(1)
                best_pkg_match = get_correct_pkg_name(pkg_name, ["py", "python"], recipe.strategy)
                if best_pkg_match is not None:
                    new_recipe.add_requirement(best_pkg_match, "host")
                    added_packages.append(best_pkg_match)

            for err_msg, (pkg_name, dep_type) in str_to_pkg.items():
                if err_msg in line_normalized and pkg_name not in added_packages:
                    new_recipe.add_requirement(pkg_name, dep_type)
                    added_packages.append(pkg_name)
        if new_recipe == recipe:
            break
        else:
            recipe = deepcopy(new_recipe)
            recipe.write_recipe_to_meta_file()
        return_code = result["StatusCode"]
        c += 1
        print("%s iteration" % c)

        if not logging.getLogger().disabled:
            src = os.path.join(recipe.path, "output")
            dst = os.path.join(recipe.path, "debug_output_files", "build_iter%d" % c)
            os.mkdir(dst)
            copytree(src, dst)

    return ((result, stdout), recipe, build_script)


def mini_iterative_test(recipe, build_script):
    print("mini iterative test started")
    new_recipe = deepcopy(recipe)
    new_build_script = deepcopy(build_script)
    c = 0
    added_packages = []
    return_code = 1
    while return_code != 0:
        result, stdout = run_conda_build_mini_test(recipe.path)
        for line_num, line in enumerate(stdout.split("\n")):
            line_normalized = line.lower()
            print(line)

            # Look for python packages
            potential_python_pkg = re.search(
                r"modulenotfounderror: no module named '(.*)'", line_normalized
            )
            if not potential_python_pkg:
                potential_python_pkg = re.search(
                    r"importerror: no module named (.*)", line_normalized
                )
            if not potential_python_pkg:
                potential_python_pkg = re.search(
                    r"pkg_resources.distributionnotfound: the '(.*)' distribution was not found", line_normalized
                )
            if not potential_python_pkg:
                potential_python_pkg = re.search(
                    r"cannot find the path for the command `(.*)`", line_normalized
                )
            if potential_python_pkg:
                pkg_name = potential_python_pkg.group(1)
                best_pkg_match = get_correct_pkg_name(pkg_name, ["py", "python"], recipe.strategy)
                if best_pkg_match is not None:
                    new_recipe.add_requirement(best_pkg_match, "run")
                    added_packages.append(best_pkg_match)

            if "versionconflict:" in line_normalized:
                pkg_with_correct_version = re.search(
                    r"requirement.parse\('(.*)'\)", line_normalized
                )
                if pkg_with_correct_version:
                    pkg_name = pkg_with_correct_version.group(1)
                    new_recipe.add_requirement(pkg_name, "run")

            for err_msg, (pkg_name, dep_type) in str_to_pkg.items():
                if err_msg in line_normalized and pkg_name not in added_packages:
                    new_recipe.add_requirement(pkg_name, dep_type)
                    added_packages.append(pkg_name)
            if "%s: command not found" % recipe.name in line_normalized:
                new_build_script.add_moving_bin_files()
            if (
                line_normalized[2:]
                in map(lambda c: c.lower(), new_recipe.test_commands)
                and "permission denied" in stdout.split("\n")[line_num + 1].lower()
            ):
                for command in new_recipe.test_commands:
                    if line_normalized[2:] in command:
                        to_call = command.split()[0]
                        new_build_script.add_chmodx("$PREFIX/bin/%s" % to_call)
            if "ModuleNotFoundError: No module named" in line:
                package_file = line.split("'")[1] + ".py"
                files = build_script.filesystem.where_is_file_in_filesystem(
                    package_file
                )
                if files:
                    new_build_script.move_file_from_source_to_bin(files[0])
            if (
                line[2:] in new_recipe.test_commands
                and "command not found" in stdout.split("\n")[line_num + 1].lower()
            ):
                for command in new_recipe.test_commands:
                    if line[2:] in command:
                        print("line[2:] in command: %s" % (line[2:] in command))
                        potential_file = command.split()[0]
                        if len(potential_file.split(".")) > 1:
                            print(
                                "len(potential_file.split('.')) > 1: %s"
                                % (len(potential_file.split(".")) > 1)
                            )
                            files = build_script.filesystem.where_is_file_in_filesystem(
                                potential_file
                            )
                            print(files)
                            if files:
                                new_build_script.move_file_from_source_to_bin(files[0])

        if new_recipe == recipe and new_build_script == build_script:
            break
        else:
            recipe = deepcopy(new_recipe)
            recipe.write_recipe_to_meta_file()
            build_script = deepcopy(new_build_script)
            build_script.write_build_script_to_file()
        return_code = result["StatusCode"]
        c += 1
        print("%s iteration" % c)

    if not logging.getLogger().disabled:
        src = os.path.join(recipe.path, "output")
        dst = os.path.join(recipe.path, "debug_output_files", "test_iter%d" % c)
        os.mkdir(dst)
        copytree(src, dst)

    return (result, stdout), recipe


def mini_sanity_check(bioconda_recipe_path, recipe):
    """ Copy build.sh and meta.yaml templates to cwd. Return a Recipe object based on the templates. """
    recipe.increment_build_number()
    recipe.write_recipe_to_meta_file()
    temp_folder_name = hashlib.md5(recipe.name.encode("utf-8")).hexdigest()
    recipes_pkg_path = os.path.join(bioconda_recipe_path, "recipes", temp_folder_name)
    real_package_name = recipe.name
    recipe.name = temp_folder_name
    recipe.write_recipe_to_meta_file()
    try:
        os.mkdir(recipes_pkg_path)
        current_recipe_path = recipe.path

        copytree(current_recipe_path, recipes_pkg_path)

        # Try to build the package
        proc = bioconda_utils_build(temp_folder_name, bioconda_recipe_path)
        for line in proc.stdout.split("\n"):
            print(line)
        if proc.returncode == 0:
            return True
        else:
            return False
    finally:
        rmtree(recipes_pkg_path)
        recipe.name = real_package_name
        recipe.write_recipe_to_meta_file()
