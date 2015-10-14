"""Module for retrieiving data from findmespot.com."""

from celery import schedules
from celery import decorators
import json
import urllib2

from app.models import position as model
from app.models import utils
from app.tasks.celery_app import celery_app


_BRENDAN_FEED = '0Ya905pdnjgy0NflhOoL0GRDzLKUJn1nf'


def GetSiteData(feed=_BRENDAN_FEED, start=0, limit=1000):
    """Return a list of Points sorted by epoch from oldest to newest."""
    print 'Retrieving site data for feed %s' % feed
    points = _RawData(feed, start, limit)
    return sorted(points, key=lambda point: point['unixTime'])


def GetFeedPositions(feed, start=0, limit=1000):
    """"Return positions for a given feed."""
    points = GetSiteData(feed, start=start, limit=limit)
    print 'Retrieved %d points for feed %s' % (len(points), feed)
    positions = []
    for point in points:
        # TODO: Store battery information.
        # TODO: Store message type.
        positions.append(model.Position(
            epoch=point['unixTime'], latitude=point['latitude'],
            longitude=point['longitude']))
    return positions


def StoreSingleFeedData(feed):
    """Store new Spot data for given feed."""
    print 'Storing data for feed %s' % feed
    positions = GetFeedPositions(feed)
    print 'Checking positions against existing for feed %s' % feed
    positions = [p for p in positions if not model.PositionAt(p.epoch).count()]
    if positions:
        print 'Saving %d new points for feed %s' % (len(positions), feed)
        model.SavePositions(positions)
        PostFetch(positions)


def PostFetch(positions):
    """Launch tasks that should be executed after fetching new data."""
    rows_dict = utils.RowsAsDicts(positions)

    # Tasks that operate on all rows.
    rows_json = json.dumps(rows_dict)
    celery_app.send_task('app.tasks.basic_geo.StoreDistanceTraversed',
                         [rows_json])

    # Tasks that only operate on a single row at a time.
    for row_dict in rows_dict:
        args = [json.dumps(row_dict)]
        celery_app.send_task('app.tasks.maps.StoreMapsInformation', args)
        celery_app.send_task('app.tasks.weather.StoreWeatherInformation', args)


# Run every 10 minutes.
# http://celery.readthedocs.org/en/latest/userguide/periodic-tasks.html
@decorators.periodic_task(
    run_every=schedules.crontab(minute='*/10'),
    time_limit=30)
def StoreNewData(feed=None, feeds=None):
    """Store new Spot data for given feed, feeds, or all feeds."""
    print 'Storing new spot data'
    if feed:
        feeds = [feed]
    if not feeds:
        feeds = [_BRENDAN_FEED]

    for feed in feeds:
        StoreSingleFeedData(feed)


def _RawData(feed, start, limit):
    """Return raw list of point messages from the given feed."""
    url = _FeedUrl(feed, start, limit)
    print 'Getting raw data for %s from url %s' % (feed, url)
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
        # This is a list, unless there's only one point - then it's a dict.
        messages = resp['feedMessageResponse']['messages']['message']
        if not isinstance(messages, list):
            messages = [messages]
        return messages
    return []


def _FeedUrl(feed, start, limit):
    return ('https://api.findmespot.com/spot-main-web/consumer/rest-api/2.0/'
            'public/feed/%s/message?start=%s&limit=%s' % (feed, start, limit))
