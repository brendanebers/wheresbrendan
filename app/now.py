"""Contains function for looking up current epoch."""

import datetime
from dateutil import relativedelta


def Now():
    """The current time."""
    return DtToEpoch(datetime.datetime.utcnow())


def DtToEpoch(dt):
    """Convert a datetime to a en epoch."""
    return (dt - datetime.datetime(1970, 1, 1)).total_seconds()


def HumanizeSeconds(delta_seconds):
    """Return a human friendly string of how much time has elapsed."""
    relative = relativedelta.relativedelta(seconds=delta_seconds)
    attrs = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']
    for attr in attrs:
        val = getattr(relative, attr)
        if val:
            return '%d %s' % (val, attr)
    return 'NO TIME AT ALL'
