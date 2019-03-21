import unittest
from bioconda_recipe_gen.bioconda_recipe_gen import return_hello, Recipe


class TestReturnHelloMethod(unittest.TestCase):
    
    def test_run(self):
        s = return_hello()
        self.assertEqual('hello', s)


class TestRecipeClass(unittest.TestCase):

    def test_add_requirement(self):
        recipe = Recipe("files_for_testing/kallisto_recipe_without_hdf5.txt")
        recipe.add_requirement("hdf5", "host")
        correct_recipe = Recipe("files_for_testing/kallisto_recipe_with_hdf5.txt")
        self.assertEqual(correct_recipe.recipe_dict, recipe.recipe_dict)

    def test_add_requirement_negative_test(self):
        recipe = Recipe("files_for_testing/kallisto_recipe_without_hdf5.txt")
        recipe.add_requirement("GARBAGE", "host")
        correct_recipe = Recipe("files_for_testing/kallisto_recipe_with_hdf5.txt")
        self.assertNotEqual(correct_recipe.recipe_dict, recipe.recipe_dict)


if __name__ == '__main__':
    unittest.main()
