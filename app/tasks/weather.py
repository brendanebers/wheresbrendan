"""Lookup weather related information."""

import forecastio  # https://pypi.python.org/pypi/python-forecastio/
import json

import config
from app import now
from app.tasks.celery_app import celery_app


def GetWeather(lat, lng):
    """Return forecastio weather object for latitude and longitude."""
    return forecastio.load_forecast(config.FORECAST_IO_API_KEY, lat, lng)


def GetCurrentWeather(lat, lng):
    """Return forecastio current weather."""
    return GetWeather(lat, lng).currently()


def GetForecastWeather(lat, lng, hours):
    """Return forecastio weather at number of hours out."""
    if hours < 0:
        raise ValueError('Forecast weather must be for the future.')
    elif hours > 48:
        raise ValueError('Forecast weather only available for 48 hours.')
    target = now.Now() + 3600 * hours  # The target timestamp.

    weather = GetWeather(lat, lng)
    hourly = weather.hourly()
    prev = hourly.data[0]
    for hour in hourly.data[1:]:
        if prev.utime <= target <= hour.utime:
            if abs(target - prev.utime) < (target - hour.utime):
                return prev
            return hour
    return hour


# This task name will be registered in app/tasks/spot.py
@celery_app.task
def StoreWeatherInformation(row_json):
    """Retrieve weather information for lat/long."""
    row = json.loads(row_json)
    current = GetCurrentWeather(row['latitude'], row['longitude'])
    data = current.d
    temperature = data['temperature']  # 27.23 (celsius) # noqa
    feels_like = data['apparentTemperature']  # noqa
    humidity = data['humiditiy']  # 0.72 for 72% # noqa
    summary = data['summary']  # like "Mostly Cloudy" # noqa
    # What's precipIntensity
    # Do I care about cloudCover
    # windSpeed might be interesting.. am I getting blown off my motorcycle?

    # Other attributes:
    # pressure, precipType, ozone, windBearing, dewPoint, precipProbability,
    # visibility
