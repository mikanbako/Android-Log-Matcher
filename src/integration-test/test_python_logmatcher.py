#!/usr/bin/env python
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

# Integration test for logmatcher on Python.

import subprocess
import unittest

import logmatcher


class TestIntegrationLogmatcher(unittest.TestCase):
    def setUp(self):
        subprocess.check_call('adb wait-for-device', shell = True)

    def executeAm(self):
        u'''
        Execute adb am.
        '''
        popen = subprocess.Popen('adb shell am start -a aaa',
            stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        popen.communicate()

    def testMatchingString(self):
        u'''
        Test when log is matched with string.
        '''
        logmatcher.start()

        self.executeAm()

        self.assert_(logmatcher.wait('Am', 10))

if __name__ == '__main__':
    unittest.main()