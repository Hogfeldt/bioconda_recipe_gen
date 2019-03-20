import unittest
from bioconda_recipe_gen.bioconda_recipe_gen import return_hello

class TestReturnHelloMethod(unittest.TestCase):
    
    def test_run(self):
        s = return_hello()
        self.assertEqual('hello', s)

if __name__ == '__main__':
    unittest.main()
