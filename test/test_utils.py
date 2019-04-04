import unittest
import sys
from bioconda_recipe_gen.utils import map_alpine_pkg_to_conda_pkg


class TestRecipeClass(unittest.TestCase):
    def test_map_alpine_pkg_to_conda_pkg_hdf5(self):
        conda_pkg = map_alpine_pkg_to_conda_pkg("hdf5")
        self.assertEqual("hdf5", conda_pkg)
        
    def test_map_alpine_pkg_to_conda_pkg_hdf5(self):
        conda_pkg = map_alpine_pkg_to_conda_pkg("zlib-dev")
        self.assertEqual("zlib", conda_pkg)

    def test_map_alpine_pkg_to_conda_pkg_negative(self):
        conda_pkg = map_alpine_pkg_to_conda_pkg("NotAPackage")
        self.assertIsNone(conda_pkg)
