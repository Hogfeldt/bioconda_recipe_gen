import os
import pkg_resources
from .recipe import Recipe
from .utils import calculate_md5_checksum, get_pkg_build_number

def cmake_recipe_factory(name, version, cmake_flags):
    recipe = Recipe(name, version)
    recipe.add_requirement("make", "build")
    recipe.add_requirement("cmake", "build")
    recipe.add_requirement("{{ compiler('c') }}", "build")
    
    flags = ""
    if cmake_flags:
        for flag in cmake_flags:
            flags = flags + "-{} ".format(flag)
    else:
        flags = "-DCMAKE_INSTALL_PREFIX=$PREFIX -DINSTALL_PREFIX=$PREFIX"
    _make_build_file(name, flags)

    return recipe


def _make_build_file(name, flags):
    """Function to make the build.sh, which
    depends on which flags should be added to the 
    template file."""
    build_template_file = pkg_resources.resource_filename(__name__, "recipes/template_build.sh")
    build_file = "%s/%s/build.sh" % (os.getcwd(), name)  
    with open(build_template_file, "r") as template:
        with open(build_file, "w") as build_file:
            for line in template:
                line = str(line)
                if line.startswith("cmake"):
                    line = "cmake .. {}\n".format(flags)
                build_file.write(line)


def add_checksum(recipe, args):
    if args.sha is not None:
        recipe.add_checksum_sha256(args.sha)
    elif args.md5 is not None:
        recipe.add_checksum_md5(args.md5)
    else:
        recipe.add_checksum_md5(calculate_md5_checksum(args.url))


def preprocess(args):
    recipe = cmake_recipe_factory(args.name, args.version, args.cmake)
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
    return recipe
