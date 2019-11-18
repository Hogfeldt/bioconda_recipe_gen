from os import getcwd
import os
import tempfile

from bioconda_recipe_gen.recipe import Recipe
from bioconda_recipe_gen.buildscript import BuildScript
from bioconda_recipe_gen.utils import (
    calculate_md5_checksum,
    get_pkg_build_number,
    download_and_unpack_source,
)
from bioconda_recipe_gen.filesystem import Filesystem


def cmake_recipe_factory(name, version):
    recipe = Recipe(name, version)
    recipe.add_requirement("make", "build")
    recipe.add_requirement("cmake", "build")
    recipe.add_requirement("{{ compiler('c') }}", "build")
    return recipe


def autoconf_recipe_factory(name, version):
    recipe = Recipe(name, version)
    recipe.add_requirement("make", "build")
    recipe.add_requirement("autoconf", "build")
    recipe.add_requirement("automake", "build")
    recipe.add_requirement("{{ compiler('c') }}", "build")
    return recipe


def python_recipe_factory(name, version):
    recipe = Recipe(name, version)
    recipe.add_requirement("python", "host")
    return recipe


def strategies_to_try(template, filesystem):
    """ Returns a list with strategies to try """
    if template == "python":
        return ["python"]
    elif template == "cmake":
        if filesystem.is_file_in_root("configure.ac"):
            return ["autoconf", "cmake"]
        else:
            return ["cmake"]
    else:
        raise NotImplemented


def build_script_factory(strategies, name, cmake_flags, filesystem):
    build_scripts = []
    for strategy in strategies:
        buildscript_path = os.path.join(os.getcwd(), name)
        build_script = BuildScript(name, buildscript_path, strategy, filesystem)
        if strategy != "python":
            flags = ""
            if cmake_flags:
                for flag in cmake_flags:
                    flags = flags + "-{} ".format(flag)
            else:
                flags = "-DCMAKE_INSTALL_PREFIX=$PREFIX -DINSTALL_PREFIX=$PREFIX"
            build_script.add_cmake_flags(flags)
        build_scripts.append(build_script)
    return build_scripts


def recipe_factory(strategies, args):
    recipes = []
    for strategy in strategies:
        if strategy == "python":
            recipe = python_recipe_factory(args.name, args.version)
        elif strategy == "autoconf":
            recipe = autoconf_recipe_factory(args.name, args.version)
        else:
            recipe = cmake_recipe_factory(args.name, args.version)
        recipe.add_source_url(args.url)
        recipe.add_build_number(
            get_pkg_build_number(recipe.name, args.bioconda_recipe_path)
        )
        add_checksum(recipe, args)
        if args.tests is not None:
            recipe.add_test_files_with_path(args.tests[0])
        if args.files is not None:
            recipe.add_test_files_with_list(args.files)
        if args.commands is not None:
            recipe.add_test_commands(args.commands)
        if args.patches is not None:
            recipe.add_patches(args.patches)
        if args.imports is not None:
            recipe.add_command_imports(args.imports)
        recipes.append(recipe)
    return recipes


def make_recipe_and_buildscript_pairs(args, filesystem):
    strategies = strategies_to_try(args.template, filesystem)
    recipes = recipe_factory(strategies, args)
    build_scripts = build_script_factory(strategies, args.name, args.cmake, filesystem)
    return recipes, build_scripts


def add_checksum(recipe, args):
    if args.sha is not None:
        recipe.add_checksum_sha256(args.sha)
    elif args.md5 is not None:
        recipe.add_checksum_md5(args.md5)
    else:
        recipe.add_checksum_md5(calculate_md5_checksum(args.url))


def preprocess(args):
    with tempfile.TemporaryDirectory() as tmpdir:
        download_and_unpack_source(args.url, tmpdir)
        source_path = os.path.join(tmpdir, "source")
        source_code_path = os.path.join(source_path, os.listdir(source_path)[0])
        filesystem = Filesystem(source_code_path)
        recipes, build_scripts = make_recipe_and_buildscript_pairs(args, filesystem)
    return recipes, build_scripts
