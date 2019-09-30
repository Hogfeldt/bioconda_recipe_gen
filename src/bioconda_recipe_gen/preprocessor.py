from os import getcwd
import pkg_resources
from .recipe import Recipe
from .buildscript import BuildScript
from .utils import calculate_md5_checksum, get_pkg_build_number

def cmake_recipe_factory(name, version):
    recipe = Recipe(name, version)
    recipe.add_requirement("make", "build")
    recipe.add_requirement("cmake", "build")
    recipe.add_requirement("{{ compiler('c') }}", "build")
    return recipe

def cmake_build_script_factory(name, cmake_flags):
    flags = ""
    if cmake_flags:
        for flag in cmake_flags:
            flags = flags + "-{} ".format(flag)
    else:
        flags = "-DCMAKE_INSTALL_PREFIX=$PREFIX -DINSTALL_PREFIX=$PREFIX"
    build_script = BuildScript("%s/%s" % (getcwd(), name))
    build_script.add_cmake_flags(flags)
    return build_script


def add_checksum(recipe, args):
    if args.sha is not None:
        recipe.add_checksum_sha256(args.sha)
    elif args.md5 is not None:
        recipe.add_checksum_md5(args.md5)
    else:
        recipe.add_checksum_md5(calculate_md5_checksum(args.url))


def preprocess(args):
    recipe = cmake_recipe_factory(args.name, args.version)
    build_script = cmake_build_script_factory(args.name, args.cmake)
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
        print(args.patches)
        recipe.add_patches(args.patches)
    return (recipe, build_script)
