import unittest
import os
import tempfile
import time #remove this when finished debugging

import bioconda_recipe_gen.build as build


#def clone_git_repo(url, dir_path):
#    cmd = "git clone %s %s" % (url, dir_path)
#    os.system(cmd)
#
#
#class TestBiocondaUtilsIterativeBuild(unittest.TestCase):
#    def setUp(self):
#        self.tmpdir = tempfile.TemporaryDirectory()
#        bioconda_recipes_repo_url = 'https://github.com/bioconda/bioconda-recipes'
#        clone_git_repo(bioconda_recipes_repo_url, self.tmpdir.name)
#
#    def test_correct_return_when_building_kallisto(self):
#        package_name = 'kallisto2'
#        bioconda_recipes_path = self.tmpdir.name
#        proc, dependencies = build.bioconda_utils_iterative_build(bioconda_recipes_path, package_name)
#        
#        self.assertEqual(proc.returncode, 0)
#        self.assertListEqual(dependencies, ['hdf5'])
#
#    def tearDown(self):
#        self.tmpdir.cleanup()


class TestMiniIterativeBuild(unittest.TestCase):
    def test_alpine_docker_build(self):
        pass

    def test_run_alpine_build(self):
        pass

    def test_exit_codes_is_success_for_kallisto(self):
        proc = build.mini_iterative_build()
        print(proc.stdout)
        pass




if __name__ == "__main__":
    unittest.main()
