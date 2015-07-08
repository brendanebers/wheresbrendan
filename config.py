import os

# For the Flask application
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
WTF_CSRF_ENABLED = True

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Celery configuration
# CELERY_BROKER_URL = os.environ.get('')
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
BROKER_CONNECTION_TIMEOUT = 30
BROKER_POOL_LIMIT = 1 # Will decrease connection usage
CELERY_ENABLE_UTC = True
CELERY_SEND_EVENTS = False
CELERY_EVENT_QUEUE_EXPIRE = 60
CELERY_EVENT_QUEUE_TTL = 10
CELERY_IGNORE_RESULT = True

# Other API keys
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
FORECAST_IO_API_KEY = os.environ.get('FORECAST_IO_API_KEY')
