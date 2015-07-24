"""Aggregates all Celery tasks into one "pretty" place."""

# flake8: noqa
from app.tasks.celery_app import celery_app  # This is our Celery object.

from app.tasks.basic_geo import *
from app.tasks.celery_app import *
from app.tasks.maps import *
from app.tasks.semantic_tagging import *
from app.tasks.spot import *
from app.tasks.texting import *
from app.tasks.weather import *
