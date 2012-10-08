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

def adb(argument):
    u'''
    Execute adb command.

    Arguments :
        argument : String of argument of adb.
    '''
    # Prevent to output log to the console.
    popen = subprocess.Popen('adb ' + argument,
        stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    popen.communicate()

class TestIntegrationLogmatcher(unittest.TestCase):
    def setUp(self):
        adb('wait-for-device')

    def testMatchingString(self):
        u'''
        Test when log is matched with string.
        '''
        logmatcher.start()

        adb('shell am start -a aaa')

        self.assert_(logmatcher.wait('Am', 10))

    def testMatchingJapaneseString(self):
        u'''
        Test when log is matched with Japanese string.
        '''
        logmatcher.start()

        adb('shell am broadcast -a ' +
            'com.github.mikanbako.androidlogmatcher.testapplication.action.JAPANESE_LOG ' +
            '--include-stopped-packages')

        self.assert_(logmatcher.wait(u'日本語のログ'))

if __name__ == '__main__':
    unittest.main()