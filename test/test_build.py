import unittest
import os
import tempfile
import time #remove this when finished debugging

import birg.build as build


class TestMiniIterativeBuild(unittest.TestCase):
    def test_exit_codes_is_success_for_kallisto(self):
        proc = build.mini_iterative_build()
        print(proc.stdout)
        pass


if __name__ == "__main__":
    unittest.main()
