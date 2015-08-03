web: gunicorn --log-file - webapp:app
worker: celery worker -A app.tasks.celery_suite --loglevel=info
beat: celery -A app.tasks.celery_suite beat
