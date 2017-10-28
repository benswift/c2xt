# -*- coding: utf-8 -*-

from .context import c2xt

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(c2xt.hmm())


if __name__ == '__main__':
    unittest.main()
