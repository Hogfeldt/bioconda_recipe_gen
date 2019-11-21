import sys
import tempfile
import hashlib
import os
from shutil import rmtree, copy2

from bioconda_utils.recipe import Recipe as bioconda_utils_Recipe

from bioconda_recipe_gen.filesystem import Filesystem
from bioconda_recipe_gen.buildscript import BuildScript
from bioconda_recipe_gen.recipe import Recipe
from bioconda_recipe_gen.utils import (
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
    recipe = Recipe(name, version, recipe_path)

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
        recipe.add_requirement(requirement, "host")
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
            recipe.add_requirement("{{compiler('c')}}", "build")
            recipe.add_requirement("cmake", "build")
            recipe.add_requirement("make", "build")
        elif strategy == "autoconf":
            recipe.add_requirement("make", "build")
            recipe.add_requirement("autoconf", "build")
            recipe.add_requirement("automake", "build")
            recipe.add_requirement("{{ compiler('c') }}", "build")
        else:
            recipe.add_requirement("python", "host")
    recipe.increment_build_number()
    return recipe


def create_build_script(recipe, args, filesystem):
    exact_buildscript_path = os.path.join(recipe.path, "build.sh")
    if os.path.isfile(exact_buildscript_path):
        build_script = BuildScript(recipe.name, args.recipe_path, "cmake", filesystem)
        with open(exact_buildscript_path, "r") as fp:
            build_script._lines = fp.readlines()
    else:
        build_script = BuildScript(recipe.name, args.recipe_path, "none", filesystem, is_none=True)
    return build_script


def preprocess(args):
    recipe = create_recipe(args.bioconda_recipe_path, args.recipe_path, args.strategy)
    with tempfile.TemporaryDirectory() as tmpdir:
        download_and_unpack_source(recipe.url, tmpdir)
        source_path = os.path.join(tmpdir, "source")
        source_code_path = os.path.join(source_path, os.listdir(source_path)[0])
        filesystem = Filesystem(source_code_path)
    build_script = create_build_script(recipe, args, filesystem)
    return ([recipe], [build_script])
