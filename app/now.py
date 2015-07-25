"""Contains function for looking up current epoch."""

import datetime
from dateutil import relativedelta


def Now():
    """The current time."""
    return (datetime.datetime.utcnow() -
            datetime.datetime(1970, 1, 1)).total_seconds()


def HumanizeSeconds(delta_seconds):
    """Return a human friendly string of how much time has elapsed."""
    relative = relativedelta.relativedelta(seconds=delta_seconds)
    attrs = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']
    result = []
    last = False
    for attr in attrs:
        val = getattr(relative, attr)
        if val:
            result.append('%d %s' % (val, attr))
            if val == 1:  # Strip off the s for singular.
                result[-1] = result[-1][:-1]
            if last:
                break
            else:
                last = True
    return ', '.join(result)
