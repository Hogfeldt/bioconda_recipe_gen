from .recipe import Recipe
from .utils import calculate_md5_checksum


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
    _make_build_file(flags)

    return recipe

def _make_build_file(flags):
    """Function to make the build.sh, which
    depends on which flags should be added to the 
    template file."""
    
    with open("src/bioconda_recipe_gen/recipes/template_build.sh", "r") as template:
        with open("src/bioconda_recipe_gen/recipes/build.sh", "w") as build_file:
            for line in template:
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
