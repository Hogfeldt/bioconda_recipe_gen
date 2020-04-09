import sys
import tempfile
import hashlib
import os
from shutil import rmtree, copy2

from bioconda_utils.recipe import Recipe as bioconda_utils_Recipe

from birg.filesystem import Filesystem
from birg.buildscript import BuildScript
from birg.recipe import Recipe
from birg.utils import (
    copytree,
    calculate_md5_checksum,
    download_and_unpack_source,
)


def create_recipe(bioconda_recipe_path, recipe_path, strategy):
    # Load meta.yaml file and instantiate Recipe object
    temp_folder_name = hashlib.md5(recipe_path.encode("utf-8")).hexdigest()
    recipes_pkg_path = os.path.join(bioconda_recipe_path, "recipes", temp_folder_name)
    try:
        os.mkdir(recipes_pkg_path)
        copytree(recipe_path, recipes_pkg_path)
        bioconda_recipe = bioconda_utils_Recipe.from_file(
            bioconda_recipe_path, recipes_pkg_path
        )
    finally:
        rmtree(recipes_pkg_path)
    name = bioconda_recipe.get("package/name")
    version = bioconda_recipe.get("package/version")
    recipe = Recipe(name, version, recipe_path, strategy)

    # Parse values from file to Recipe object
    try:
        recipe.add_source_url(bioconda_recipe.get("source/url"))
    except KeyError:
        sys.exit(
            "No source url was found in the given meta.yaml file, please add a source url"
        )
    recipe.add_build_number(bioconda_recipe.get("build/number", "0"))
    try:
        recipe.add_checksum_sha256(bioconda_recipe.get("source/sha256"))
    except KeyError:
        recipe.add_checksum_md5(
            bioconda_recipe.get(
                "source/md5", calculate_md5_checksum(bioconda_recipe.get("source/url"))
            )
        )
    build_requirements = bioconda_recipe.get("requirements/build", [])
    for requirement in build_requirements:
        recipe.add_requirement(requirement, "build")
    host_requirements = bioconda_recipe.get("requirements/host", [])
    for requirement in host_requirements:
        recipe.add_requirement(requirement, "host", host_only=True)
    run_requirements = bioconda_recipe.get("requirements/run", [])
    for requirement in run_requirements:
        recipe.add_requirement(requirement, "run")
    try:
        recipe.add_test_commands(bioconda_recipe.get("test/commands"))
    except KeyError:
        pass
    try:
        recipe.add_test_files_with_list(bioconda_recipe.get("test/files"))
    except KeyError:
        pass
    try:
        recipe.add_patches_with_list(bioconda_recipe.get("source/patches"), recipe_path)
    except KeyError:
        pass
    # Conda will not accept the compiler dependency given by bioconda
    try:
        build_requirements = recipe.recipe_dict["requirements"]["build"]
        if "compiler_c" in build_requirements:
            recipe.recipe_dict["requirements"]["build"].remove("compiler_c")
            recipe.recipe_dict["requirements"]["build"].append("{{compiler('c')}}")
        if "compiler_cxx" in build_requirements:
            recipe.recipe_dict["requirements"]["build"].remove("compiler_cxx")
            recipe.recipe_dict["requirements"]["build"].append("{{compiler('cxx')}}")
    except KeyError:
        if strategy == "cmake":
            recipe.add_requirement("{{ compiler('c') }}", "build")
            recipe.add_requirement("cmake", "build")
            recipe.add_requirement("make", "build")
        elif strategy == "autoconf":
            recipe.add_requirement("make", "build")
            recipe.add_requirement("autoconf", "build")
            recipe.add_requirement("automake", "build")
            recipe.add_requirement("{{ compiler('c') }}", "build")
    if strategy.startswith("python"):
        try:
            host_environment = recipe.recipe_dict["requirements"]["host"]
            if not any(map(lambda req: req.startswith("python"), host_environment)):
                if strategy == "python2":
                    recipe.add_requirement("python =2.7", "host")
                else:
                    recipe.add_requirement("python >=3", "host")
        except KeyError:
            if strategy == "python2":
                    recipe.add_requirement("python =2.7", "host")
            else:
                recipe.add_requirement("python >=3", "host")
    try:
        recipe.script = bioconda_recipe.get("build/script")
    except KeyError:
        pass
    try:
        recipe.add_command_imports(bioconda_recipe.get("test/imports"))
    except KeyError:
        pass
    try:
        recipe.add_entry_point(bioconda_recipe.get("build/entry_points"))
    except KeyError:
        pass
    try:
        recipe.add_noarch(bioconda_recipe.get("build/noarch"))
    except KeyError:
        pass
    try:
        recipe.add_test_requires(bioconda_recipe.get("test/requires"))
    except KeyError:
        pass
    recipe.increment_build_number()
    return recipe


def create_build_script(recipe, args, filesystem):
    if recipe.script is None:
        build_script = BuildScript(recipe.name, args.recipe_path, args.strategy, filesystem)
        exact_buildscript_path = os.path.join(recipe.path, "build.sh")
        with open(exact_buildscript_path, "r") as fp:
            build_script._lines = fp.readlines()
    else:
        build_script = BuildScript(recipe.name, args.recipe_path, args.strategy, filesystem, recipe.script)
    return build_script


def preprocess(args, bioconda_recipe_path):
    recipe = create_recipe(bioconda_recipe_path, args.recipe_path, args.strategy)
    with tempfile.TemporaryDirectory() as tmpdir:
        download_and_unpack_source(recipe.url, tmpdir)
        source_path = os.path.join(tmpdir, "source")
        source_code_path = os.path.join(source_path, os.listdir(source_path)[0])
        filesystem = Filesystem(source_code_path)
    build_script = create_build_script(recipe, args, filesystem)
    return ([recipe], [build_script])
