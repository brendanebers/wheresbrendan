"""Methods for sending text messages and twilio responses."""

from twilio import rest
from twilio import twiml

import config


def _GetClient():
    return rest.TwilioRestClient(
        config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)


def SendMessage(message):
    """Send a message to Brendan."""
    client = _GetClient()
    # Returns a message object, I'm not sure what its purpose is.
    client.messages.create(
        to=config.BRENDAN_NUMBER, from_=config.TWILIO_NUMBER, body=message)


def GetResponse(message=None):
    """Create a response to a twilio API call."""
    resp = twiml.Response()
    if message:
        resp.message(message)
    return resp
