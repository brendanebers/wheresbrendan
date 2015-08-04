web: gunicorn --log-file - webapp:app
worker: celery worker -A app.tasks.celery_suite --loglevel=info --without-heartbeat
beat: celery beat -A app.tasks.celery_suite
