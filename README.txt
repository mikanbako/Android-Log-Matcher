Android Log Matcher - A Python module to check whether string appears in logcat

Overview :

    Android Log Matcher checks whether a string or a string that matched with
    regular expression pattern appears in an output of "adb logcat".
    For example, To check whether
    "START {act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER]"
    appears in log to check launching activity, write as follows.

        import logmatcher

        logmatcher.start()

        # ... (Activity launching)

        print logmatcher.wait(
            'START {act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER]')

    In this case, if the string appears in log, logmatcher.wait() returns True.

Required software :

    * Android SDK Tools Revision 20 or above (http://developer.android.com/)

    * One of the below list.

        * Python 2.7

        * monkeyrunner

        * Jython 2.5

Usage :

    1. Put logmatcher.py to the same directory that contains your scripts.

    2. Import logmatcher module to your scripts.

        import logmatcher

    3. Call logmatcher.start() just before a watched procedure.

    4. Call logmatcher.wait() with a string or
       logmatcher.waitPattern() with a regular expression pattern after
       the watched procedure.

    5. Check the return value of these functions. logmatcher.wait() returns
       True if the string is found in the log. logmatcher.waitPattern() returns
       Match object if there is a string matched with the pattern in the log.

API Reference :

    logmatcher.start(logcatArgument = u'')

        Start watching logcat.

        Argument :

            logcatArgument :
                A str or unicode value that represents argument of
                "adb logcat".

    logmatcher.wait(match, timeout = defaultTimeout)

        Wait until the string is found in the watching log.

        Arguments :

            match : A str or unicode value that is searched the watching log.

            timeout : A float value that represents seconds for timeout.

        Return :

            True if the string is found in the watching log before timeout,
            False otherwise.

    logmatcher.waitPattern(pattern, timeout = defaultTimeout)

        Wait until a string that matched with the pattern is found in
        the watching log.

        Argument :

            pattern : A str or unicode that represents regular
                expression pattern, or a compiled regular expression pattern
                value that searched from the watching log.

            timeout : A float value that represents seconds for timeout.

        Return :

            Match object if such a string is found in the watching log
            before timeout, None otherwise.

    logmatcher.defaultTimeout

        A float value that represents seconds for timeout.

        Default value is 5 (seconds).

Tips :

    * Specify logcat format by logcatArgument of logmatcher.start for
      accuracy or speed.
