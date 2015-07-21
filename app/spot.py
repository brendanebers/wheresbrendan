"""Module for retrieiving data from findmespot.com.

Exposes:
    Point: A namedtuple for a latitude/longitude at a specific time.
    GetData: Method for retrieving data for a given feed.
"""

import collections
import json
import urllib2


Point = collections.namedtuple('Point', ['epoch', 'latitude', 'longitude'])


_BRENDAN_FEED = '0Ya905pdnjgy0NflhOoL0GRDzLKUJn1nf'


def GetData(feed=_BRENDAN_FEED, start=0, limit=1000):
    """Return a list of Points sorted by epoch from oldest to newest."""
    raw = _RawData(feed, start, limit)
    data = _ParseRaw(raw)
    return sorted(data, key=lambda point: point.epoch)


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
    return data['response']['feedMessageResponse']['messages']['message']


def _ParseRaw(raw):
    """Parse the json string returned by the spot website."""
    for p in raw:
        yield Point(epoch=p['unixTime'], latitude=p['latitude'],
                    longitude=p['longitude'])


_URL = ('https://api.findmespot.com/spot-main-web/consumer/rest-api/2.0/'
        'public/feed/%s/message?start=%s&limit=%s')


def _FeedUrl(feed, start, limit):
    return _URL % (feed, start, limit)
