#!/usr/bin/env monkeyrunner
# coding: UTF-8

# Copyright 2012 Keita Kita
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Define test suite for integration test on monkeyrunner.
#
# This test suite is on run monkeyrunner with Android 4.1.

import os
import sys

sys.path.extend(os.environ['PYTHONPATH'].split(os.pathsep))

import unittest

import device
import test_monkeyrunner_logmatcher

def suite():
    loader = unittest.TestLoader()

    return unittest.TestSuite(
        [loader.loadTestsFromModule(test_monkeyrunner_logmatcher)])

if __name__ == '__main__':
    device.init()
    unittest.TextTestRunner(verbosity = 2).run(suite())