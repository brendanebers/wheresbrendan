"""This module is used by gunicorn to launch the web app."""
from app import flask_app  # The app must be imported first.
from app import views  # This registers the views with the flask app

# A necessary evil; gunicorn needs need a Flask object within the module.
app = flask_app.flask_app


def Run(*args, **kwargs):
    flask_app.flask_app.run(*args, **kwargs)
