web: gunicorn --log-file - webapp:app
worker: celery worker -A app.tasks.celery_suite --loglevel=info --without-hearbeat
beat: celery beat -A app.tasks.celery_suite
