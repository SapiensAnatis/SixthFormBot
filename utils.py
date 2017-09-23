import datetime
import os

__maindirectory__ = os.path.dirname(__file__)

"""Used for outputting messages with timestamps and severity/source descriptors. Should always be used over lone print statements."""
def log(message, source, severity="info"):
    print(f"[{datetime.datetime.now():%H:%M:%S}][{severity}] {source}: {message}")

def localize_filepath(filepath):
    return os.path.join(__maindirectory__, filepath)