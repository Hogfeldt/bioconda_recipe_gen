from os import getcwd
import os
import tempfile
from copy import deepcopy

from .recipe import Recipe
from .buildscript import BuildScript
from .utils import calculate_md5_checksum, get_pkg_build_number, download_and_unpack_source
from .filesystem import Filesystem


def cmake_recipe_factory(name, version):
    recipe = Recipe(name, version)
    recipe.add_requirement("make", "build")
    recipe.add_requirement("cmake", "build")
    recipe.add_requirement("{{ compiler('c') }}", "build")
    return recipe


def templates_to_try(filesystem):
    """ Returns a list with templates to try """
    if filesystem.is_file_in_root("configure.ac"):
        return ["template_build_autoreconf.sh", "template_build_cmake.sh"]
    else:
        return ["template_build_cmake.sh"]


def cmake_build_script_factory(name, cmake_flags, filesystem):
    templates = templates_to_try(filesystem)
    build_scripts = []
    for template in templates:
        build_script = BuildScript(name, "%s/%s" % (getcwd(), name), template, filesystem)
        flags = ""
        if cmake_flags:
            for flag in cmake_flags:
                flags = flags + "-{} ".format(flag)
        else:
            flags = "-DCMAKE_INSTALL_PREFIX=$PREFIX -DINSTALL_PREFIX=$PREFIX"
        build_script.add_cmake_flags(flags)
        build_scripts.append(build_script)
    return build_scripts


def add_checksum(recipe, args):
    if args.sha is not None:
        recipe.add_checksum_sha256(args.sha)
    elif args.md5 is not None:
        recipe.add_checksum_md5(args.md5)
    else:
        recipe.add_checksum_md5(calculate_md5_checksum(args.url))


def preprocess(args):
    # download source code for project
    with tempfile.TemporaryDirectory() as tmpdir:
        download_and_unpack_source(args.url, tmpdir)
        source_path = "%s/source" % tmpdir
        source_code_path = "%s/%s" % (source_path, os.listdir(source_path)[0])
        filesystem = Filesystem(source_code_path)
        recipe = cmake_recipe_factory(args.name, args.version)
        build_scripts = cmake_build_script_factory(args.name, args.cmake, filesystem)

    recipe.add_source_url(args.url)
    recipe.add_build_number(get_pkg_build_number(recipe.name, args.bioconda_recipe_path))
    add_checksum(recipe, args)
    if args.tests is not None:
        recipe.add_test_files_with_path(args.tests[0])
    if args.files is not None:
        recipe.add_test_files_with_list(args.files)
    if args.commands is not None:
        recipe.add_test_commands(args.commands)
    if args.patches is not None:
        recipe.add_patches(args.patches)

    recipes = []
    for i in range(len(build_scripts)):
        recipes.append(deepcopy(recipe))
    return recipes, build_scripts
