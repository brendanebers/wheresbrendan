"""Basic geography functions for bird-flies distance and speed calculations."""

from geopy import distance
import json
import math

from app.models import position as model
from app.models import utils as model_utils
from app.tasks.celery_app import celery_app


class _Deltas(object):

    """Calculate distance, elapsed time, and rate between two positiions."""

    def __init__(self, pos_1, pos_2):
        """"Accept Position objects or dictionaries."""
        def Get(obj, attr):
            if hasattr(obj, '__getitem__'):
                return obj[attr]
            return getattr(obj, attr)

        dist = distance.vincenty(
            (Get(pos_1, 'latitude'), Get(pos_1, 'longitude')),
            (Get(pos_2, 'latitude'), Get(pos_2, 'longitude')))
        self.meters = dist.meters
        self.time = abs(Get(pos_1, 'epoch') - Get(pos_2, 'epoch'))
        self.rate = self.meters / self.time

    def UpdateRow(self, row):
        """Update Position row with distance, rate, and elapsed time."""
        def Set(obj, attr, val):
            if hasattr(obj, 'attr') or not hasattr(obj, '__setitem__'):
                setattr(obj, attr, val)
            else:
                obj[attr] = val

        Set(row, 'distance_from_prev', self.meters)
        Set(row, 'time_from_prev', self.time)
        Set(row, 'speed_from_prev', self.rate)


def CalculateDistance(coord1, coord2):
    """Return distance, in meters, between two coordinates."""
    return distance.vincenty(coord1, coord2).meters


def ConvenientDistance(pos1, pos2):
    return CalculateDistance((pos1.latitude, pos1.longitude),
                             (pos2.latitude, pos2.longitude))


def CalculateBearing(coord1, coord2):
    """Return bearing from coord1 to coord2."""
    # Stolen from: http://stackoverflow.com/a/17662363
    lat1, lng1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lng2 = math.radians(coord2[0]), math.radians(coord2[1])

    d_lon = lng2 - lng1
    y = math.sin(d_lon) * math.cos(lat2)
    x = (math.cos(lat1) * math.sin(lat2) -
         math.sin(lat1)*math.cos(lat2)*math.cos(d_lon))
    return math.degrees(math.atan2(y, x))


_BEARINGS = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW',
             'WSW', 'W', 'WNW', 'NW', 'NNW']


def ReadableBearing(bearing):
    """Return a human readable bearing."""
    # Stolen from: http://stackoverflow.com/a/7490772
    if bearing < 0:
        bearing += 360
    index = int((bearing / 22.5) + .5)
    print bearing, index
    return _BEARINGS[index % 16]


# This task's name is registered in app/tasks/spot.py
@celery_app.task
def StoreDistanceTraversed(rows_json):
    """Calculate and save the distance and time traveled for multiple rows."""
    rows = json.loads(rows_json)

    # Most recent first.
    rows.sort(key=lambda r: r['epoch'], reverse=True)
    if not rows:
        return 0

    previous = model.GetLastPositions(1, rows[-1]['epoch'])
    rows.extend(model_utils.RowsAsDicts(previous))

    if len(rows) < 2:
        return 0  # Can't compare distances between 1 object.

    deltas = {}
    for idx, row in enumerate(rows[:-1]):  # Don't calculate delta for last row.
        deltas[row['id']] = _Deltas(row, rows[idx+1])

    print deltas

    # Update the rows in the database.
    row_objs = model.GetPositionsByIds(deltas.keys())
    for row in row_objs:
        deltas[row.id].UpdateRow(row)
    model.UpdatePositions(row_objs)
    return len(row_objs)
