import unittest
import bioconda_recipe_gen.bioconda_recipe_gen as brg


class TestReturnHelloMethod(unittest.TestCase):
    
    def test_run(self):
        s = brg.return_hello()
        self.assertEqual('hello', s)


if __name__ == '__main__':
    unittest.main()
