#!/usr/bin/env python

"""test_randogen.py
"""

import unittest

from randogen import RandoGen

class TestRandoGen(unittest.TestCase):
    def setUp(self):
        self.r = RandoGen()

    def test_generate_randos(self):
        for n in range(10):
            self.assertEqual(len(self.r.fetch_randos(n, return_bytes=False)), n)

if __name__ == '__main__':
    unittest.main()
