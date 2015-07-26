"""Module for retrieiving data from findmespot.com."""

from celery import schedules
from celery import decorators
import json
import urllib2

from app import models
from app.flask_app import db
from app.tasks.celery_app import celery_app


_BRENDAN_FEED = '0Ya905pdnjgy0NflhOoL0GRDzLKUJn1nf'


def GetSiteData(feed=_BRENDAN_FEED, start=0, limit=1000):
    """Return a list of Points sorted by epoch from oldest to newest."""
    points = _RawData(feed, start, limit)
    return sorted(points, key=lambda point: point['unixTime'])


def GetFeedPositions(feed, start=0, limit=1000):
    """"Return positions for a given feed."""
    points = GetSiteData(feed, start=start, limit=limit)
    positions = []
    for point in points:
        # TODO: Store battery information.
        # TODO: Store message type.
        positions.append(models.Position(
            epoch=point['unixTime'], latitude=point['latitude'],
            longitude=point['longitude']))
    return positions


def StoreSingleFeedData(feed):
    """Store new Spot data for given feed."""
    positions = GetFeedPositions()
    positions = [p for p in positions if not models.PositionAt(p.epoch).count()]
    if positions:
        for position in positions:
            db.session.add(p)
        db.session.commit()
        PostFetch(positions)


def PostFetch(positions):
    """Launch tasks that should be executed after fetching new data."""
    rows_json = json.dumps(models.RowsAsDicts(positions))
    celery_app.send_task('app.tasks.basic_geo.StoreDistanceTraversed',
                         rows_json)


# Run every 10 minutes.
# http://celery.readthedocs.org/en/latest/userguide/periodic-tasks.html
@decorators.periodic_task(run_every=schedules.crontab(minute='*/10'))
def StoreNewData(feed=None, feeds=None):
    """Store new Spot data for given feed, feeds, or all feeds."""
    if feed:
        feeds = [feed]
    if not feeds:
        feeds = models.GetFeeds()

    for feed in feeds:
        StoreSingleFeedData(feed)


def _RawData(feed, start, limit):
    """Return raw list of point messages from the given feed."""
    url = _FeedUrl(feed, start, limit)
    resp = urllib2.urlopen(url)
    data = json.loads(resp.read())
    # raw_point_message = {
    #    'longitude': -122.27261,
    #    'unixTime': 1433018300,
    #    'messageDetail': '',
    #    'messageType': 'TRACK',
    #    'dateTime': '2015-05-30T20:38:20+0000',
    #    'showCustomMsg': 'N',
    #    'messengerName': 'The Hurricane',
    #    'messengerId': '0-2492928',
    #    'batteryState': 'GOOD',
    #    'latitude': 37.82813,
    #    'hidden': 0,
    #    'modelId': 'SPOT3',
    #    'id': 400011957,
    #    '@clientUnixTime': '0'
    # }
    resp = data['response']
    if 'feedMessageResponse' in resp:  # No points available
        return resp['feedMessageResponse']['messages']['message']
    return []


def _FeedUrl(feed, start, limit):
    return ('https://api.findmespot.com/spot-main-web/consumer/rest-api/2.0/'
            'public/feed/%s/message?start=%s&limit=%s' % (feed, start, limit))