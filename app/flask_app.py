"""Creates the Flask object and database objects."""
import flask
from flask.ext import sqlalchemy

import config

flask_app = flask.Flask(__name__)
flask_app.config.from_object('config')

db = sqlalchemy.SQLAlchemy(flask_app)
