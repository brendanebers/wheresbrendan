web: gunicorn --log-file - webapp:app
worker: celery worker -A app.tasks.celery_suite --loglevel=info --heartbeat-interval=90
beat: celery beat -A app.tasks.celery_suite
