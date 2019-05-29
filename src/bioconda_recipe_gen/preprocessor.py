from .recipe import Recipe
from .utils import calculate_md5_checksum


def cmake_recipe_factory(name, version):
    recipe = Recipe(name, version)
    recipe.add_requirement("make", "build")
    recipe.add_requirement("cmake", "build")
    recipe.add_requirement("{{ compiler('c') }}", "build")
    return recipe


def add_checksum(recipe, args):
    if args.sha is not None:
        recipe.add_checksum_sha256(args.sha)
    elif args.md5 is not None:
        recipe.add_checksum_md5(args.md5)
    else:
        recipe.add_checksum_md5(calculate_md5_checksum(args.url))


def preprocess(args):
    recipe = cmake_recipe_factory(args.name, args.version)
    recipe.add_source_url(args.url)
    add_checksum(recipe, args)
    if args.tests is not None:
        recipe.add_tests(args.tests[0])
    if args.commands is not None:
        recipe.add_test_commands(args.commands)
    if args.patches is not None:
        print(args.patches)
        recipe.add_patches(args.patches)
    return recipe
