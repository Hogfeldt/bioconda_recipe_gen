import sys
import tempfile
import hashlib
import os
from shutil import rmtree, copy2

from bioconda_utils.recipe import Recipe as bioconda_utils_Recipe

from bioconda_recipe_gen.filesystem import Filesystem
from bioconda_recipe_gen.buildscript import BuildScript
from bioconda_recipe_gen.recipe import Recipe
from bioconda_recipe_gen.utils import copytree, calculate_md5_checksum, download_and_unpack_source


def create_recipe(bioconda_recipe_path, recipe_path):
    # Load meta.yaml file and instantiate Recipe object
    temp_folder_name = hashlib.md5(recipe_path.encode("utf-8")).hexdigest()
    recipes_pkg_path = "%s/recipes/%s/" % (bioconda_recipe_path, temp_folder_name)
    try:
        os.mkdir(recipes_pkg_path)

        for item in os.listdir(recipe_path):
            s = os.path.join(recipe_path, item)
            d = os.path.join(recipes_pkg_path, item)

            if not os.path.isdir(s):
                copy2(s, d)
            elif item != "output":
                copytree(s, d)

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
    # Conda will not accept the compiler dependency given by bioconda
    build_requirements = recipe.recipe_dict['requirements']['build']
    if 'compiler_c' in build_requirements:
        recipe.recipe_dict['requirements']['build'].remove("compiler_c")
        recipe.recipe_dict['requirements']['build'].append("{{compiler('c')}}")
    if 'compiler_cxx' in build_requirements:
        recipe.recipe_dict['requirements']['build'].remove("compiler_cxx")
        recipe.recipe_dict['requirements']['build'].append("{{compiler('cxx')}}")
    return recipe


def create_build_script(recipe, args, filesystem):
    build_script = BuildScript(
        recipe.name, args.recipe_path, "cmake", filesystem
    )
    with open(build_script.path+"/build.sh", "r") as fp:
        build_script._lines = []
        for line in fp.readlines():
            build_script._lines.append(line)
    return build_script


def preprocess(args):
    recipe = create_recipe(args.bioconda_recipe_path, args.recipe_path)
    with tempfile.TemporaryDirectory() as tmpdir:
        download_and_unpack_source(recipe.url, tmpdir)
        source_path = "%s/source" % tmpdir
        source_code_path = "%s/%s" % (source_path, os.listdir(source_path)[0])
        filesystem = Filesystem(source_code_path)
    build_script = create_build_script(recipe, args, filesystem)
    return ([recipe], [build_script])
