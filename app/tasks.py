import celery
from celery import schedules
from celery import decorators
import forecastio
from geolocation import google_maps
from geopy import distance
import json
import unidecode

import config
from app import models
from app import spot
from app.flask_app import db


celery_app = celery.Celery(__name__, broker=config.CELERY_BROKER_URL)
celery_app.config_from_object('config')


# Run every 10 minutes.
# http://celery.readthedocs.org/en/latest/userguide/periodic-tasks.html
@decorators.periodic_task(run_every=schedules.crontab(minute='*/10'))
def ScrapeData(feed=None, feeds=None):
    """Scrapes and saves data for the given feed or feeds."""
    if feed:
        feeds = [feed]
    if not feeds:
        feeds = models.GetFeeds()

    for feed in feeds:
        data = spot.GetData(limit=1000)
        points = [
            models.Position(
                epoch=p.epoch, latitude=p.latitude, longitude=p.longitude)
            for p in data]
        points = [p for p in points if not models.PositionAt(p.epoch).count()]
        if points:
            for p in points:
                db.session.add(p)
            db.session.commit()
            PostFetch(points)


def PostFetch(points):
    """Async launches tasks that should be executed after fetching new data."""
    rows_json = json.dumps(models.RowsAsDicts(points))
    # DistanceTraversed.delay(rows_json)
    # GeoInformation.delay(rows_json)
    # WeatherInformation.delay(rows_json)


class _Deltas(object):
    """Calculates distance, elapsed time, and rate between two positiions."""

    def __init__(self, pos_1, pos_2):
        """"Accepts Position objects or dictionaries."""

        def Get(obj, attr):
            if hasattr(obj, '__getitem__'):
                return obj[attr]
            return getattr(obj, attr)

        dist = distance.vincenty(
            (Get(pos_1, 'latitude'), Get(pos_1, 'longitude')),
            (Get(pos_2, 'latitude'), Get(pos_2, 'longitude')))
        self.meters = dist.meters
        self.time = abs(Get(pos_1, 'epoch') - Get(pos_2, 'epoch'))
        self.speed = self.meters / self.time

    def UpdateRow(self, row):
        """Updates Position row with distance, rate, and elapsed time."""

        def Set(obj, attr, val):
            if hasattr(obj, '__setitem__'):
                obj[attr] = val
            setattr(obj, val)

        Set(row, 'distance_from_prev', self.meters)
        Set(row, 'time_from_prev', self.time)
        Set(row, 'speed_from_prev', self.rate)


@celery_app.task
def DistanceTraversed(rows_json):
    """Calculates and saves the distance and time traveled."""
    rows = json.loads(rows_json)

    # Most recent first.
    rows.sort(key=lambda r: r['epoch'], reverse=True)
    if not rows:
        return

    rows.extend([r for r in models.GetLastPositions(1, rows[-1].epoch)])

    if len(rows) < 2:
        return  # Can't compare distances between 1 object.

    for idx, row in enumerate(rows[:-1]):
        delta = _Delta(row, rows[idx+1])
        delta.UpdateRow(row)

    for row in rows[:-1]:
        pass  # Save changes to these rows.

    TagMovementStates.delay(json.dumps(rows[:-1]))


@celery_app.task
def GeoInformation(rows_json):
    """Looks up geo information for given lat/long."""
    # Look at https://pypi.python.org/pypi/geopy
    # from geopy.geocoders import Nominatim
    # geolocator = Nominatim()
    # location = geolocator.reverse("52.509669, 13.376294")

    # Wasn't happy with the geopy results using Nominatim
    # Alternatives make use of Google Maps
    # https://pypi.python.org/pypi/geolocation-python/0.2.0
    # https://pypi.python.org/pypi/pygeocoder
    rows = json.loads(rows_json)
    if not rows:
        return
    row = rows[0]

    maps = google_maps.GoogleMaps(api_key=config.GOOGLE_API_KEY)
    location = maps.search(lat=row['latitude'], lng=row['longitude'])
    # location seems to hold a set of different location possibilities?
    loc = location.first()

    # Attributes: administrative_area, city, country, country_shortcut,
    # formatted_address, postal_code, route, street_number

    # The data comes in ascii strings, so you might see something weird like
    # this:
    # >>> loc.city
    # 'Mazatl\xc3\xa1n'

    # So we can improve it by doing
    # >>> city = unicode(loc.city, 'utf-8')  # the utf-8 part is necessary
    # >>> city
    # u'Mazatl\xe1n'
    # >>> print city
    # Mazatla'n  # (where a has an accent on it)

    # Potentially be a problem with things that don't handle ascii
    # >>> city_ascii = unidecode.unidecode(city)
    # >>> print city_ascii
    # Mazatlan
    city = unicode(loc.city, 'utf-8')  # this can be encoded strangely.
    city_ascii = unidecode.unidecode(city)

    country = unicode(loc.country, 'utf-8')
    country_ascii = unidecode.unidecode(country)


@celery_app.task
def WeatherInformation(rows_json):
    """Retrieves weather information for lat/long."""
    # Look at https://pypi.python.org/pypi/pyql-weather/0.1  # Doesn't work
    # https://pypi.python.org/pypi/python-forecastio/

    lat = -31.967819
    lng = 115.87718

    rows = json.loads(rows_json)
    row = rows[0]
    forecast = forecastio.load_forecast(
        config.FORECAST_IO_API_KEY, row['latitude'], row['longitude'])
    current = forecast.currently()
    data = current.d
    temperature = data['temperature']  # 27.23 celsius
    feels_like = data['apparentTemperature']
    humidity = data['humiditiy']  # 0.72 for 72%
    summary = data['summary']  # like "Mostly Cloudy"
    # What's precipIntensity
    # Do I care about cloudCover
    # windSpeed might be interesting.. am I getting blown off my motorcycle?

    # Other attributes:
    # pressure, precipType, ozone, windBearing, dewPoint, precipProbability,
    # visibility

@celery_app.task
def TagMovementStates(rows_json):
    """Guesses if the recent points are stopped, moving, etc."""
    # stopped: speed <= 0.25 m/s
    # moving: .25 m/s < speed || distance > (10*60*.25) and time > 30 minutes
    # so, it's moving if its moving, or if there's been a gap of transmissions.
    # slow: .25 m/s < speed <= 4 m/s
    # fast: 4 m/s < speed
    # jumped: distance > 500m and time > 30 minutes
    rows = json.loads(rows_json)
    for row in rows:
        tags = set()
        if row['speed_from_prev'] <= 0.25:
            tags.add('stopped')
        if row['speed_from_prev'] > 0.25:
            tags.add('moving')
            if tags['speed_from_prev'] > 4:
                tags.add('fast')
            else:
                tags.add('slow')

        if tags['distance_from_prev'] >= 100 and tags['time'] > 30*60:
            tags.add('moving')

        if tags['distance_from_prev'] > 1000 and tags['time'] > 30*60:
            tags.add('jumped')
