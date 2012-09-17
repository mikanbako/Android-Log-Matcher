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

# A module that monitors logcat and checks whether logs are matched.
#
# This module can be run on Jython 2.5 with monkeyrunner.

from __future__ import with_statement

import os
import platform
import signal
import subprocess
from threading import Event, Thread, RLock

### Version Depending Function ###

def kill(popen):
    u'''
    Kill process of Popen object.

    Arguments :
        process : Popen object that be killed.
    '''

    # Kill the process via an internal object (java.lang.Process) of
    # Popen in Jython.
    #
    # Because Popen does not have PID in Jython 2.5 and therefore os.kill
    # cannot be used.
    # See http://python.6.n6.nabble.com/subprocess-pid-td1766477.html

    popen._process.destroy()

###

class LogcatThread(Thread):
    u'''
    Thread that runs logcat.
    '''

    def __init__(self, logListener):
        u'''
        Constructor.

        Run logcat.

        Argument :
            logListener : Listener for log.
                This listener has onLogReceived(line).
        '''
        Thread.__init__(self, name = u'LogcatThread')

        # Start logcat after clear log.
        #
        # Do not start logcat in run(). Because run() runs on a created thread
        # and log is forgotten between start() and run().
        subprocess.Popen(
            u'adb logcat -c', stdout = subprocess.PIPE, shell = True).wait()
        self.__adb = subprocess.Popen(
            u'adb logcat', stdout = subprocess.PIPE, shell = True)

        # Lock object for this thread.
        self.__lock = RLock()

        self.__logListener = logListener
        self.__isTerminated = False

    def run(self):
        # If this thread has already terminated, finish this thread.
        with self.__lock:
            if self.__isTerminated:
                return

        # Notice received log until this thread is terminated.
        with self.__adb.stdout as logcat:
            for line in logcat:
                self.__logListener.onLogReceived(line)

                with self.__lock:
                    if self.__isTerminated:
                        break

    def terminate(self):
        u'''
        Request terminating this thread.
        '''

        # Raise the termination flag.
        with self.__lock:
            isNeededProcessTerminating = not self.__isTerminated
            self.__isTerminated = True

        # Terminate adb process.
        if isNeededProcessTerminating:
            kill(self.__adb)


class LogMatcher:
    u'''
    Monitor and match log from logcat.
    '''

    def start(self):
        u'''
        Start logcat.
        '''
        self.__matchedEvent = self.createMatchedEvent()
        self.__logcatThread = self.createLogcatThread()
        self.__lock = RLock()
        self.__log = u''
        self.__match = None

        self.__logcatThread.start()

    def createLogcatThread(self):
        u'''
        Create LogcatThread.

        This method is for testability.
        '''
        return LogcatThread(self)

    def createMatchedEvent(self):
        u'''
        Create Event for matching.

        This method is for testability.
        '''
        return Event()

    def wait(self, match, timeout):
        u'''
        Wait called thread until log is matched.

        Arguments:
            match : Matching string.
            timeout : Seconds until timeout.
        '''

        # Set matching.
        with self.__lock:
            self.__match = unicode(match)

        try:
            # If the log has already matched, return immediately.
            if self.isMatched():
                return True

            # Wait matching until timeout.
            self.__matchedEvent.wait(timeout)
        finally:
            self.__logcatThread.terminate()

        return self.__matchedEvent.isSet()

    def onLogReceived(self, line):
        u'''
        Called when line is received.

        This method is called by other thread.
        '''

        # Store the line.
        with self.__lock:
            self.__log += unicode(line)

        # If the line is matched, terminate the logcat and
        # wake the waiting event.

        if self.isMatched():
            self.__logcatThread.terminate()
            self.__matchedEvent.set()

    def isMatched(self):
        u'''
        Check whether the log is matched.

        This method may be called by other thread.
        '''
        with self.__lock:
            if self.__match:
                return 0 <= self.__log.find(self.__match)
            else:
                return False

class LogMatcherRunningException(Exception):
    u'''
    Raised when the LogMatcher is running.
    '''
    pass

# Global LogMatcher.
currentLogcatMatcher = None

def start():
    u'''
    Start log matcher.

    Exception :
        LogMatcherRunningException : When log matcher is running.
    '''

    global currentLogcatMatcher

    # Check whether global LogMatcher is running.
    # If it is running, an exception is raised.
    if currentLogcatMatcher:
        raise LogMatcherRunningException()

    currentLogcatMatcher = LogMatcher()
    currentLogcatMatcher.start()

def wait(match, timeout):
    u'''
    Wait matching.

    Arguments :
        match : Matching string.
        timeout : Timeout seconds.
    Return :
        True if the matching string is matched with log.
        False if the matching string is not matched until timeout.
    '''

    global currentLogcatMatcher

    result = currentLogcatMatcher.wait(match, timeout)
    currentLogcatMatcher = None

    return result
