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

# Integration test for logmatcher on monkeyrunner.

import os
import sys

sys.path.extend(os.environ['PYTHONPATH'].split(os.pathsep))

import unittest
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

import device
import logmatcher

class TestIntegrationLogMatcher(unittest.TestCase):
    def executeAmWithDummyArgument(self):
        u'''
        Execute adb am.
        '''
        device.get().shell(u'am start -a aaa')

    def testMatchingString(self):
        u'''
        Test when log is matched with string.
        '''
        logmatcher.start(u'*:D')

        self.executeAmWithDummyArgument()

        self.assert_(logmatcher.wait('Am'))

    def testMatchingJapaneseString(self):
        u'''
        Test when log is matched with Japanese string.
        '''
        logmatcher.start()

        device.get().shell(
            u'am broadcast -a ' +
            u'com.github.mikanbako.androidlogmatcher.testapplication.action.JAPANESE_LOG ' +
            u'--include-stopped-packages')

        self.assert_(logmatcher.wait(u'日本語のログ'))

    def testMatchingPattern(self):
        u'''
        Test when log is matched with pattern.
        '''
        logmatcher.start()

        self.executeAmWithDummyArgument()

        self.assertEquals(u'com.android.commands.am.Am',
            logmatcher.waitPattern(ur'\s([.a-zA-z]+?\.Am)').group(1))

    def testMatchingJapanesePattern(self):
        u'''
        Test when log is matched with Japanese pattern.
        '''
        logmatcher.start()

        device.get().shell(
            u'am broadcast -a ' +
            u'com.github.mikanbako.androidlogmatcher.testapplication.action.JAPANESE_LOG ' +
            u'--include-stopped-packages')

        self.assert_(logmatcher.waitPattern(ur'日本語.ログ'))

    def testNoMatched(self):
        u'''
        Test when log is not matched.
        '''
        self.executeAmWithDummyArgument()
        logmatcher.start()

        self.assert_(not logmatcher.wait('Am', 1))

    def testNoMatchedWithLogLevel(self):
        u'''
        Test when log is not matched because level of matched log is lower.
        '''
        self.executeAmWithDummyArgument()
        logmatcher.start(u'*:I')

        device.get().shell(u'am aaa')

        self.assert_(not logmatcher.wait('Am', 2))

    def testDuplicateStarting(self):
        u'''
        Test when logmatcher is started duplicative.

        logmatcher.start raises LogMatcherRunningException.
        '''

        logmatcher.start()
        try:
            self.assertRaises(
                logmatcher.LogMatcherRunningException, logmatcher.start)
        finally:
            # Force termination logmatcher.
            logmatcher.wait('', 0)

    def testWaitingWhenNotStarted(self):
        u'''
        Test when logmatcher tries to wait when it is not started.

        logmatcher.wait raises LogMatcherNotStartedException.
        '''

        self.assertRaises(
            logmatcher.LogMatcherNotStartedException, logmatcher.wait, '')

if __name__ == '__main__':
    device.init()
    unittest.main()