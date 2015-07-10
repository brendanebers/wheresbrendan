from twilio import rest
import twilio.twiml

import config


def _GetClient():
    return rest.TwilioRestClient(
        config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)


def SendMessage(message):
    """Sends a message to Brendan."""
    client = _GetClient()
    text_msg = client.messages.create(
        to=config.BRENDAN_NUMBER, from_=config.TWILIO_NUMBER, body=message)


def HandleIncoming(from):
    resp = twilio.twiml.Response()
    resp.message = 'Handled'
    print resp
    return resp
