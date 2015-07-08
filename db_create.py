#!flask/bin/python
"""TODO: Document / clean this up."""
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from app import config import SQLALCHEMY_MIGRATE_REPO
from app.flask_app import db
import os

if not os.path.exists(config.SQLALCHEMY_MIGRATE_REPO):
    api.create(config.SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(config.SQLALCHEMY_DATABASE_URI,
        config.SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(config.SQLALCHEMY_DATABASE_URI,
        config.SQLALCHEMY_MIGRATE_REPO,
        api.version(config.SQLALCHEMY_MIGRATE_REPO))
