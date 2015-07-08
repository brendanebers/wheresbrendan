web: gunicorn --log-file - webapp:app
worker: celery worker -A app.tasks --beat --loglevel=info
