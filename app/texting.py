from twilio import rest

import config


def _GetClient():
    return rest.TwilioRestClient(
        config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)


def SendMessage(message):
    """Sends a message to Brendan."""
    client = _GetClient()
    text_msg = client.messages.create(
        to=config.BRENDAN_NUMBER, from_=config.TWILIO_NUMBER, body=message)
