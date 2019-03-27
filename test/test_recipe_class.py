import unittest
from bioconda_recipe_gen.recipe import Recipe


class TestRecipeClass(unittest.TestCase):
    def test_initialization_method(self):
        #recipe = Recipe("test/files_for_testing/")
        pass

    def test_add_requirement(self):
        recipe = Recipe("test/files_for_testing/kallisto_recipe_without_hdf5.txt")
        recipe.add_requirement("hdf5", "host")
        correct_recipe = Recipe("test/files_for_testing/kallisto_recipe_with_hdf5.txt")
        self.assertEqual(correct_recipe.recipe_dict, recipe.recipe_dict)

    def test_add_requirement_negative_test(self):
        recipe = Recipe("test/files_for_testing/kallisto_recipe_without_hdf5.txt")
        recipe.add_requirement("GARBAGE", "host")
        correct_recipe = Recipe("test/files_for_testing/kallisto_recipe_with_hdf5.txt")
        self.assertNotEqual(correct_recipe.recipe_dict, recipe.recipe_dict)

    # test multiple adds to a recipe
    # test the init method
    # test the write to file method
