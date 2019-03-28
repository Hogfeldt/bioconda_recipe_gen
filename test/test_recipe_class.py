import unittest
from bioconda_recipe_gen.recipe import Recipe


class TestRecipeClass(unittest.TestCase):
    def test_initialization_method(self):
        recipe = Recipe("test/files_for_testing/full_kallisto_recipe.yaml")
        self.assertEqual("test/files_for_testing/full_kallisto_recipe.yaml", recipe.path_to_meta_file)
        self.assertEqual(recipe.recipe_dict["package"]["name"], "kallisto")
        self.assertEqual(recipe.recipe_dict["package"]["version"], "0.45.0")
        self.assertEqual(recipe.recipe_dict["source"]["url"], "https://github.com/pachterlab/kallisto/archive/v0.45.0.tar.gz")
        self.assertEqual(recipe.recipe_dict["source"]["sha256"], "42cf3949065e286e0a184586e160a909d7660825dbbb25ca350cb1dd82aafa57") 
        self.assertEqual(recipe.recipe_dict["build"]["number"], 0) 
        self.assertEqual(recipe.recipe_dict["requirements"]["build"].sort(), ["cmake", "{{ compiler('cxx') }}", "autoconf", "automake"].sort()) 
        self.assertEqual(recipe.recipe_dict["requirements"]["host"], ["hdf5", "zlib"]) 
        self.assertEqual(recipe.recipe_dict["requirements"]["run"], ["hdf5", "zlib"]) 
        self.assertEqual(recipe.recipe_dict["test"]["files"], ["t.fa", "t.fq"]) 
        self.assertEqual(recipe.recipe_dict["test"]["commands"], ["kallisto version"]) 
        self.assertEqual(recipe.recipe_dict["about"]["home"], "http://pachterlab.github.io/kallisto") 
        self.assertEqual(recipe.recipe_dict["about"]["license"], "BSD_2_Clause") 
        self.assertEqual(recipe.recipe_dict["about"]["summary"], "Quantifying abundances of transcripts from RNA-Seq data, or more generally of target sequences using high-throughput sequencing reads.") 
        self.assertEqual(recipe.recipe_dict["extra"]["identifiers"], ["biotools:kallisto", "doi:10.1038/nbt.3519"]) 

    def test_add_requirement(self):
        # This test assumes that the initialization test passes
        recipe = Recipe("test/files_for_testing/kallisto_recipe_without_hdf5.txt")
        recipe.add_requirement("hdf5", "host")
        correct_recipe = Recipe("test/files_for_testing/kallisto_recipe_with_hdf5.txt")
        self.assertEqual(correct_recipe.recipe_dict, recipe.recipe_dict)

    def test_add_requirement_negative_test(self):
        # This test assumes that the initialization test passes
        recipe = Recipe("test/files_for_testing/kallisto_recipe_without_hdf5.txt")
        recipe.add_requirement("GARBAGE", "host")
        correct_recipe = Recipe("test/files_for_testing/kallisto_recipe_with_hdf5.txt")
        self.assertNotEqual(correct_recipe.recipe_dict, recipe.recipe_dict)

    # test multiple adds to a recipe
    # test the write to file method - should give a bug because of the
    #   different syntax that we convert to be able to read it. (need to convert back)
    #   remember to copy the correct recipe into the test folder
