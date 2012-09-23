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
import re
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

# Default waiting timeout.
defaultTimeout = 5

class LogcatThread(Thread):
    u'''
    Thread that runs logcat.
    '''

    def __init__(self, logListener, logcatArgument):
        u'''
        Constructor.

        Run logcat.

        Argument :
            logListener : Listener for log.
                This listener has onLogReceived(line).
            logcatArgument : String of arguments for logcat.
        '''
        Thread.__init__(self, name = u'LogcatThread')

        # Start logcat after clear log.
        #
        # Do not start logcat in run(). Because run() runs on a created thread
        # and log is forgotten between start() and run().
        subprocess.Popen(
            u'adb logcat -c ' + logcatArgument, stdout = subprocess.PIPE,
            shell = True).wait()
        self.__adb = subprocess.Popen(
            u'adb logcat ' + logcatArgument, stdout = subprocess.PIPE,
            shell = True)

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

    def start(self, logcatArgument = u''):
        u'''
        Start logcat.

        Arguments:
            logcatArgument : String of arguments for logcat.
        '''
        self.__matchedEvent = self.createMatchedEvent()
        self.__logcatThread = self.createLogcatThread(logcatArgument)
        self.__lock = RLock()
        self.__log = u''
        self.__matchFunction = (lambda log: False)

        self.__logcatThread.start()

    def createLogcatThread(self, logcatArgument):
        u'''
        Create LogcatThread.

        This method is for testability.

        Arguments:
            logcatArgument : String of arguments for logcat.
        '''
        return LogcatThread(self, logcatArgument)

    def createMatchedEvent(self):
        u'''
        Create Event for matching.

        This method is for testability.
        '''
        return Event()

    def waitFunction(self, matchFunction, timeout= defaultTimeout):
        u'''
        Wait called thread until log is matched from the function.

        If matchFunction returns not None or not False,
        this method also return it.

        Arguments:
            matchFunction : Matching function.
                It has an argument that received log.
                This function may be called by other thread.
            timeout : Seconds until timeout.
        '''

        # Set matching.
        with self.__lock:
            self.__matchFunction = matchFunction

        try:
            # If the log has already matched, return immediately.
            result = self.checkMatched()
            if result:
                return result

            # Wait matching until timeout.
            self.__matchedEvent.wait(timeout)
        finally:
            self.__logcatThread.terminate()

        return self.checkMatched()


    def wait(self, match, timeout = defaultTimeout):
        u'''
        Wait called thread until log is found.

        Arguments:
            match : Searching string.
            timeout : Seconds until timeout.
        Exception :
            ValueError : If type of match is not str or unicode.
        '''

        # Verify argument.
        if not isinstance(match, basestring):
            raise ValueError(u'match type is ' + unicode(type(match)))

        return self.waitFunction(
            lambda log: 0 <= log.find(unicode(match)), timeout)

    def waitPattern(self, pattern, timeout = defaultTimeout):
        u'''
        Wait called thread until log is found with pattern.

        Arguments :
            pattern : Searching pattern. str or unicode,
                compiled regular expression pattern.
            timeout : Seconds until timeout.
        '''

        # Convert compiled regex pattern if pattern is basestring.
        if isinstance(pattern, basestring):
            waitingPattern = re.compile(unicode(pattern))
        else:
            waitingPattern = pattern

        return self.waitFunction(
            lambda log: waitingPattern.search(log), timeout)

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

        if self.checkMatched():
            self.__logcatThread.terminate()
            self.__matchedEvent.set()

    def checkMatched(self):
        u'''
        Check whether the log is matched.

        This method may be called by other thread.
        '''
        with self.__lock:
            return self.__matchFunction(self.__log)

class LogMatcherRunningException(Exception):
    u'''
    Raised when the LogMatcher is running.
    '''
    pass

# Global LogMatcher.
currentLogcatMatcher = None

def start(logcatArgument = u''):
    u'''
    Start log matcher.

    Arguments :
        logcatArgument : String of arguments for logcat.
    Exception :
        LogMatcherRunningException : When log matcher is running.
    '''

    global currentLogcatMatcher

    # Check whether global LogMatcher is running.
    # If it is running, an exception is raised.
    if currentLogcatMatcher:
        raise LogMatcherRunningException()

    currentLogcatMatcher = LogMatcher()
    try:
        currentLogcatMatcher.start(logcatArgument)
    except:
        currentLogcatMatcher = None

def waitFunction(waitFunction):
    u'''
    Wait using a result of the function.

    It has an argument that receives an instance of LogMatcher.

    Arguments :
        waitFunction : A function for waiting.
    Return :
        Result of the wait function.
    '''

    global currentLogcatMatcher

    try:
        result = waitFunction(currentLogcatMatcher)
    finally:
        currentLogcatMatcher = None

    return result

def wait(match, timeout = defaultTimeout):
    u'''
    Wait finding.

    Arguments :
        match : Searching string.
        timeout : Timeout seconds.
    Return :
        True if the matching string is matched with log.
        False if the matching string is not matched until timeout.
    '''

    return waitFunction(lambda logMatcher: logMatcher.wait(match, timeout))

def waitPattern(pattern, timeout = defaultTimeout):
    u'''
    Wait finding with pattern.

    Arguments :
        pattern : Searching compiled regular expression pattern.
            This argument must be str or unicode,
            compiled regular expression pattern.
        timeout : Timeout seconds.
    Return :
        Match object if the pattern is matched with log.
        None if the pattern is not matched with log.
    '''

    return waitFunction(
        lambda logMatcher: logMatcher.waitPattern(pattern, timeout))