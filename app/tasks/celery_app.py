"""Contains the initialization of the celery app."""

import celery

import config


celery_app = celery.Celery(__name__, broker=config.CELERY_BROKER_URL)
celery_app.config_from_object('config')
