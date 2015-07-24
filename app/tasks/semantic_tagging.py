"""Create tags for positions."""

import json

from app.tasks.celery_app import celery_app


def GetCrowFliesTags(row):
    """Return a set of tags describing the crow-flies movement."""
    tags = set()
    if row['speed_from_prev'] <= 0.25:
        tags.add('stopped')
    if row['speed_from_prev'] > 0.25:
        tags.add('moving')
        if tags['speed_from_prev'] > 2.5:  # 9km/h, 5.6mph
            tags.add('fast')
        else:
            tags.add('slow')

    if tags['distance_from_prev'] >= 100 and tags['time_from_prev'] > 30*60:
        tags.add('moving')

    if tags['distance_from_prev'] > 5000 and tags['time_from_prev'] > 31*60:
        tags.add('jumped')

    if tags['time_from_prev'] > 31*60:
        tags.add('resume')

    return tags


# This name will be registered in app/tasks/basic_geo.py
@celery_app.task
def StoreCrowFliesTags(row_json):
    """Store the crow-flies movement tags with the given row."""
    row = json.loads(row_json)
    GetCrowFliesTags(row)
