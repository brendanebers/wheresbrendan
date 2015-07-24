#!flask/bin/python
"""Generates database migration scripts based on changes to model classes."""

import imp
import os

from migrate.versioning import api
from app.flask_app import db
from app import models  # Just making sure they're loaded. # flake8: noqa
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO


def main():
    print "Reading database version..."
    current_version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    next_version = current_version + 1

    # Generate name for next migration script
    new_migration_name = '%03d_migration.py' % next_version
    migration = os.path.join(SQLALCHEMY_MIGRATE_REPO, 'versions', new_migration_name)

    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    exec(old_model, tmp_module.__dict__)

    script = api.make_update_script_for_model(
        SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
    fh = open(migration, 'wt')
    fh.write('from sqlalchemy.dialects.postgresql import *\n')
    fh.write(script)
    fh.close()

    print 'New migration saved as ', migration
    print 'Dont forget to upgrade the database:'
    print '  python db_repository/manage.py upgrade'


if __name__ == '__main__':
    main()
