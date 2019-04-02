import unittest
import bioconda_recipe_gen.build as build


class TestAlpineIterativeBuild(unittest.TestCase):
   def test_alpine_docker_build(self):
       pass

   def test_run_alpine_build(self):
       pass

   def test_exit_codes_is_success_for_kallisto(self):
       src = "https://github.com/pachterlab/kallisto/archive/v0.45.0.tar.gz"
       proc, dependencies = build.alpine_iterative_build(src)

       cmake_passed = "cmake pass" in proc.stdout
       make_passed = "make pass" in proc.stdout
       make_install_passed = "make install pass" in proc.stdout

       self.assertTrue(cmake_passed)
       self.assertTrue(make_passed)
       self.assertTrue(make_install_passed)
       self.assertListEqual(dependencies, ['g++', 'gcc', 'make', 'cmake', 'zlib-dev', 'autoconf', 'hdf5-dev'])


class TestAlpineTestOnRuntime(unittest.TestCase):
    def test_alpine_run_test_with_kallisto(self):
        src = "https://github.com/pachterlab/kallisto/archive/v0.45.0.tar.gz"
        build_dependencies = [
            "g++",
            "gcc",
            "make",
            "cmake",
            "zlib-dev",
            "autoconf",
            "hdf5-dev",
        ]
        test = "kallisto version"

        result, dependencies = build.alpine_run_test(src, build_dependencies, test)
        self.assertTrue(result)
        self.assertListEqual(dependencies, ['g++', 'gcc', 'hdf5'])


if __name__ == "__main__":
    unittest.main()
