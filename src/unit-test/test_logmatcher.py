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

# Test for matching part of LogMatcher.

import dummy_threading
import re
import threading
import unittest

import logmatcher

class MockLogcatThread(dummy_threading.Thread):
    u'''
    LogcatThread that does not execute adb.
    '''

    def __init__(self):
        dummy_threading.Thread.__init__(self)
        self.isTerminated = False

    def terminate(self):
        self.isTerminated = True

class MockLogMatcher(logmatcher.LogMatcher):
    u'''
    LogMatcher that creates MockLogcatThread.
    '''

    def createLogcatThread(self, logcatArgument):
        return MockLogcatThread()

    def createMatchedEvent(self):
        return dummy_threading.Event()

class TestMatchingLog(unittest.TestCase):
    u'''
    Test matching log.
    '''

    def setUp(self):
        logmatcher.defaultTimeout = 2
        self.__matcher = MockLogMatcher()
        self.__matcher.start()

    def testFirstMatched(self):
        u'''
        LogMatcher does not match just after LogMatcher is created.
        '''
        self.assert_(not self.__matcher.checkMatched())

    def testIllegalMatchArgument(self):
        u'''
        ValueError is raised when wait receives no basestring value.
        '''
        self.assertRaises(
            ValueError, self.__matcher.wait, self.__matcher, re.compile('a'))

    def testNotMatchedStringWhenNoLog(self):
        u'''
        LogMatcher does not match when it did not receive any log.
        '''
        self.assert_(self.__matcher.wait(u'match', 0.1) == False)

    def testNotMatchedStringWhenNotMatchedLog(self):
        u'''
        LogMatcher does not match when it did not receive matched log.
        '''
        self.__matcher.onLogReceived('matched')

        self.assert_(self.__matcher.wait(u'not matched', 0.1) == False)

    def testMatchedStringBeforeWaiting(self):
        u'''
        LogMatcher matches before waiting to receive log.
        '''
        self.__matcher.onLogReceived('matc')
        self.__matcher.onLogReceived('hing')

        self.assert_(self.__matcher.wait(u'match', 0.1) == True)

    def testMatchedStringAfterWaiting(self):
        u'''
        LogMatcher matches after waiting to receive log.
        '''
        def sendLog(logMatcher):
            logMatcher.onLogReceived("matched")

        threading.Timer(1, sendLog, [self.__matcher]).start()
        self.assert_(self.__matcher.wait(u'match') == True)

    def testNotMatchedPatternWhenNotMatchedLog(self):
        u'''
        LogMatcher does not match pattern when it did not receive matched log.
        '''
        self.__matcher.onLogReceived('matched')

        self.assert_(
            self.__matcher.waitPattern(
                re.compile(ur'not matched'), 0.1) is None)

    def testMatchedPatternBeforeWaiting(self):
        u'''
        LogMatcher matches pattern before waiting to receive log.
        '''
        self.__matcher.onLogReceived('ba123b')

        self.assertEqual(u'123',
            self.__matcher.waitPattern(re.compile(ur'a(\d+)b')).group(1))

    def testMatchedPatternAfterWaiting(self):
        u'''
        LogMatcher matches after waiting to receive log.
        '''
        def sendLog(logMatcher):
            logMatcher.onLogReceived('a123b')

        threading.Timer(1, sendLog, [self.__matcher]).start()
        self.assertEquals(u'123',
            self.__matcher.waitPattern(ur'a(\d{3})b').group(1))

if __name__ == '__main__':
    unittest.main()