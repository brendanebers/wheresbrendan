"""Handles GETs and POSTS from Twilio."""

from flask import request

import config
from app.flask_app import flask_app as app
from app.tasks import texting


@app.route('/api/texting/', methods=['GET', 'POST'])  # GET for local testing.
def HandleTexts():
    """Handle POSTs from Twilio."""
    from_number = request.values.get('From')
    message = request.values.get('Body')
    response = _ParseText(from_number, message)
    return str(response or texting.GetResponse())


def _ParseText(from_number, original_message):
    lowered = original_message.lower().split(None, 1)
    if not lowered:  # If they aren't going to talk to us...
        raise ValueError('Text message cannot be empty.')

    command = lowered[0]
    message = (lowered[1] if len(lowered) == 2 else '').strip()

    if command.startswith('weather'):
        return _WeatherRequest(from_number, message)

    elif command.startswith('where'):
        return _WhereRequest(from_number, message)


def _WhereRequest(from_number, message):
    """Respond where a tracked spot is.

    Args:
        from_number: The number that sent the request.
        message: The message, stripped of the command. Initially ignored, but
            could be used in the future if a person is following multiple Spots.

    Returns:
        A twiml Response or None.
    """


def _WeatherRequest(from_number, message):
    """Respond with weather info of current location, destination, or between.

    This method responds asynchronously to valid requests.

    Args:
        from_number: The number that sent the request, should correspond with a
            tracked Spot.
        message: The message, stripped of the "weather" command. If empty, the
            weather at current location will be sent. If the message is just
            location, like "Mexico city", then the weather at Mexico City will
            be sent. If the message is "to Mexico City", then a temp range and
            chance of rain between current location and Mexico City will be
            sent.

    Returns:
        A twiml Response or None.
    """
    if from_number == config.BRENDAN_NUMBER:
        pass
