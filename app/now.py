"""Contains function for looking up current epoch."""

import datetime


def Now():
    """The current time."""
    return (datetime.datetime.utcnow() -
            datetime.datetime(1970, 1, 1)).total_seconds()
