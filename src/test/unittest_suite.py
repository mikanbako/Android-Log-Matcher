#!/usr/bin/env python
# coding: UTF-8

# Define test suite for unit test.

import os.path
import unittest

def suite():
    u"""
    Define unit test.
    """
    test_loader = unittest.TestLoader()
    return test_loader.discover(os.path.dirname(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())

