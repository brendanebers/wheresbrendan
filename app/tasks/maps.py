"""Functions for interacting with maps and geo data."""

from geolocation.google_maps import GoogleMaps
import json
import unidecode

import config
from app.tasks import basic_geo
from app.tasks.celery_app import celery_app


def _Client():
    return GoogleMaps(api_key=config.GOOGLE_API_KEY)


def SearchByLatLng(lat, lng):
    """Perform a maps search by lat lng."""
    maps = _Client()
    results = maps.search(lat=lat, lng=lng)
    return results


def SearchByName(name):
    """Perform a maps search by name."""
    maps = _Client()
    return maps.search(name)


def SearchByNameNear(name, lat, lng):
    """Search by name and return results sorted by distance to lat/lng."""
    locations = SearchByName(name).all()
    coord = (lat, lng)
    results = []
    for loc in locations:
        dist = basic_geo.CalculateDistance(coord, (loc.lat, loc.lng)) / 1000
        bearing = basic_geo.CalculateBearing(coord, (loc.lat, loc.lng))
        readable_bearing = basic_geo.ReadableBearing(bearing)
        results.append((dist, readable_bearing, loc))
    results.sort(key=lambda res: res[0], reverse=False)
    return results


# This task's name will be registered in app/tasks/spot.py
@celery_app.task
def StoreMapsInformation(row_json):
    """Store location information for a given row."""
    row = json.loads(row_json)
    results = SearchByLatLng(row['latitude'], row['longitude'])
    loc = results.first()

    city = unicode(loc.city, 'utf-8')  # this can be encoded strangely.
    city_ascii = unidecode.unidecode(city)  # noqa

    country = unicode(loc.country, 'utf-8')
    country_ascii = unidecode.unidecode(country)  # noqa

    # There's currently a bug in the administrative_area code. I would like to
    # store state or province or whatever. I did some test searched for
    # "Santa Fe near Guadalajara" and they would show roads and stores and it
    # was a mess. Searching "Santa Fe near Jalisco" gave me the small town
    # nearby. (Searching for "Santa Fe" just gave me the New Mexico one.)


def MapsDistance(current, previous):
    """Return the driving distance between two points."""
    _Client()


# This will be registered with app/tasks/spot.py
@celery_app.task
def StoreMapDistance(row_json):
    """Store the map distance for the current row from previous."""
    # This might be modified in the future to support "on_foot"
