#!flask/bin/python
"""TODO: Document / clean this up."""
from migrate.versioning import api
import os

import config
from app.models import db_models  # Just making sure they're loaded. # noqa


if __name__ == '__main__':
    if not os.path.exists(config.SQLALCHEMY_MIGRATE_REPO):
        api.create(config.SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(
            config.SQLALCHEMY_DATABASE_URI,
            config.SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(
            config.SQLALCHEMY_DATABASE_URI,
            config.SQLALCHEMY_MIGRATE_REPO,
            api.version(config.SQLALCHEMY_MIGRATE_REPO))
