"""This module is used by gunicorn to launch the web app."""
from app import flask_app  # The app must be imported first.

# This registers the views and public apis with with the flask app
from app import twilio_api  # noqa
from app import views  # noqa


# A necessary evil; gunicorn needs need a Flask object within the module.
app = flask_app.flask_app


if __name__ == '__main__':
    app.run(debug=True)
