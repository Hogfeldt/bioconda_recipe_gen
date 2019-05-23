from .recipe import Recipe


def cmake_recipe_factory(name, version):
    recipe = Recipe(name, version)
    recipe.add_requirement("make", "build")
    recipe.add_requirement("cmake", "build")
    recipe.add_requirement("{{ compiler('c') }}", "build")
    return recipe


def preprocess(args):
    recipe = cmake_recipe_factory(args.name, args.version)
    recipe.add_source_url(args.url)
    if args.sha is not None:
        recipe.add_checksum_sha256(args.sha)
    if args.md5 is not None:
        recipe.add_checksum_md5(args.md5)
    if args.tests is not None:
        recipe.add_tests(args.tests[0])
    if args.commands is not None:
        recipe.add_test_commands(args.commands)
    if args.patches is not None:
        print(args.patches)
        recipe.add_patches(args.patches) 
    return recipe
