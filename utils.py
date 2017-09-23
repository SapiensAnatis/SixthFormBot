"""
The intention of utils.py is to provide handy functions without having any dependencies
within the project which does not depend on the project in any way. Functions in here are
generally used in order to save long lines of code from being used to perform tasks which
are repeated often.
"""

import datetime
import os

__maindirectory__ = os.path.dirname(__file__)

def log(message, source, severity="info"):
    """
    Used for outputting messages with timestamps and severity/source descriptors.
    Should always be used over lone print statements.

    Keyword args:
    message -- the message to log to the console
    source -- a description of where the log function is being invoked
    severity -- a string describing the severity, e.g. info, debug, error, warning (default info)
    """

    print(f"[{datetime.datetime.now():%H:%M:%S}][{severity}] {source}: {message}")
