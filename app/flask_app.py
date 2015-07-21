"""Creates the Flask object and database objects."""

import flask
from flask.ext import sqlalchemy

import config  # Ensure that the import works. # noqa


flask_app = flask.Flask(__name__)
flask_app.config.from_object('config')

db = sqlalchemy.SQLAlchemy(flask_app)
