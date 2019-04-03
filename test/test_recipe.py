import unittest
import shutil
import os
import filecmp
from bioconda_recipe_gen.recipe import Recipe


class TestRecipeClass(unittest.TestCase):

    def setUp(self):
        self.kallisto_dict = {
            'package': 
                {'name': 'kallisto', 
                'version': '0.45.0'},
            'source': 
                {'url': 'https://github.com/pachterlab/kallisto/archive/v0.45.0.tar.gz', 
                'sha256': '42cf3949065e286e0a184586e160a909d7660825dbbb25ca350cb1dd82aafa57'}, 
            'build': 
                {'number': 0}, 
            'requirements': 
                {'build': ['cmake', 'autoconf', 'automake', "{{ compiler('cxx') }}"], 
                'host': ['hdf5', 'zlib'], 
                'run': ['hdf5', 'zlib']}, 
            'test': 
                {'files': ['t.fa', 't.fq'], 
                'commands': ['kallisto version']},
            'about': 
                {'home': 'http://pachterlab.github.io/kallisto', 
                'license': 'BSD_2_Clause', 
                'summary': 'Quantifying abundances of transcripts from RNA-Seq data, or more generally of target sequences using high-throughput sequencing reads.'}, 
            'extra': 
                {'identifiers': ['biotools:kallisto', 'doi:10.1038/nbt.3519']}}

    def test_initialization_method(self):
        recipe = Recipe("test/files_for_testing/full_kallisto_recipe.yaml")
        self.assertDictEqual(recipe.recipe_dict, self.kallisto_dict)

    def test_write_recipe_to_meta_file(self):
        temp_file_path = "test/files_for_testing/temp.yaml"
        kallisto_file_path = "test/files_for_testing/full_kallisto_recipe.yaml" 
        simple_file_path = "test/files_for_testing/simple_recipe.yaml"
        
        # making a copy of the simple recipe, to avoid overriding 
        # the simple recipe when writing to it with write_recipe_to_meta_file
        shutil.copy(simple_file_path, temp_file_path)
        recipe = Recipe(temp_file_path)
        
        # override the loaded dict with the kallisto dict that
        # matches the full_kallisto_recipe.yaml file
        recipe.recipe_dict = self.kallisto_dict
        recipe.write_recipe_to_meta_file()

        with open(temp_file_path, "r") as temp_file:
            temp_data = temp_file.read().strip().replace(" ", "").replace("\n", "")
        with open(kallisto_file_path, "r") as kallisto_file:
            kallisto_data = kallisto_file.read().replace(" ", "").replace("\n", "")
    
        self.assertTrue(temp_data == kallisto_data)
        
        # clean up
        os.remove(temp_file_path)

    def test_add_requirement(self):
        recipe = Recipe("test/files_for_testing/kallisto_recipe_with_hdf5.txt")
        self.assertListEqual(recipe.recipe_dict["requirements"]["build"], ["cmake", "make"])
        self.assertListEqual(recipe.recipe_dict["requirements"]["host"], ["hdf5"])
        self.assertRaises(KeyError, lambda: recipe.recipe_dict["requirements"]["run"])

        recipe.add_requirement("firstRequirement", "build")
        recipe.add_requirement("secRequirement", "build")
        self.assertListEqual(recipe.recipe_dict["requirements"]["build"], ["cmake", "make", "firstRequirement", "secRequirement"]) 

        recipe.add_requirement("firstRequirement", "host")
        recipe.add_requirement("secRequirement", "host")
        self.assertListEqual(recipe.recipe_dict["requirements"]["host"], ["hdf5", "firstRequirement", "secRequirement"])  

        recipe.add_requirement("firstRequirement", "run")
        recipe.add_requirement("secRequirement", "run")
        self.assertListEqual(recipe.recipe_dict["requirements"]["run"], ["firstRequirement", "secRequirement"])   