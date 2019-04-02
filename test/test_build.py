import unittest
import bioconda_recipe_gen.build as build


class TestApineIterativeBuild(unittest.TestCase):
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
        self.assertListEqual(dependencies, ['zlib-dev', 'autoconf', 'hdf5-dev'])


if __name__ == "__main__":
    unittest.main()
