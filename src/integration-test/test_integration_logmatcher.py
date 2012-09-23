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

# Integration test for logmatcher.

import os
import sys

sys.path.extend(os.environ['PYTHONPATH'].split(os.pathsep))

import unittest
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

import device
import logmatcher

class TestIntegrationLogMatcher(unittest.TestCase):
    def testMatchingString(self):
        logmatcher.start()

        device.get().shell(u'am aaa')

        self.assert_(logmatcher.wait('Am'))

    def testMatchingPattern(self):
        logmatcher.start()

        device.get().shell(u'am aaa')

        self.assertEquals(u'com.android.commands.am.Am',
            logmatcher.waitPattern(ur'\s([.a-zA-z]+?\.Am)').group(1))

    def testNoMatched(self):
        logmatcher.start()

        self.assert_(not logmatcher.wait('Am', 1))

if __name__ == '__main__':
    device.init()
    unittest.main()