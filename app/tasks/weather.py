"""Lookup weather related information."""

import forecastio  # https://pypi.python.org/pypi/python-forecastio/
import json

import config
from app import now
from app.models import position as position_model
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


# This task name is registered in app/tasks/spot.py
@celery_app.task
def StoreWeatherInformation(row_json):
    """Retrieve weather information for lat/long."""
    row_dict = json.loads(row_json)
    current = GetCurrentWeather(row_dict['latitude'], row_dict['longitude'])
    data = current.d

    row = position_model.GetPositionsByIds([row_dict['id']]).first()
    if not row:
        print 'Row %s not found when storing weather info' % row_dict['id']

    row.temperature = data['temperature']  # 27.23 (celsius) # noqa
    row.apparent_temperature = data['apparentTemperature']  # noqa
    row.humidity = data['humidity']  # 0.72 for 72% # noqa
    row.weather_summary = data['summary']  # like "Mostly Cloudy" # noqa
    row.precip_probability = data['precipProbability']
    row.precip_intensity = data['precipIntensity']
    row.precip_type = data.get('precipType', '')
    row.wind_speed = data['windSpeed']
    # What's precipIntensity
    # Do I care about cloudCover
    # windSpeed might be interesting.. am I getting blown off my motorcycle?

    # Other attributes:
    # pressure, precipType, ozone, windBearing, dewPoint, precipProbability,
    # visibility
