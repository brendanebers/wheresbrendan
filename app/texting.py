"""Methods for sending and parsing text messages."""

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


def HandleIncoming(from_number, original_message):
    """Route an incoming text message.

    Args:
        from_number: The sender of the text message.
        original_message: The body of the message.

    Returns:
        A twiml Response.
    """
    empty = twiml.Response()
    lowered = original_message.lower().split(None, 1)
    if not lowered:  # If they aren't going to talk to us...
        return empty

    command = lowered[0]
    message = lowered[1] if len(lowered) == 2 else ''

    if command.startswith('weather'):
        return _RespondWeather(from_number, message) or empty

    elif command.startswith('where'):
        return _RespondWhere(from_number, message) or empty

    return empty


def _RespondWhere(from_number, message):
    """Respond where a tracked spot is.

    Args:
        from_number: The number that sent the request.
        message: The message, stripped of the command. Initially ignored, but
            could be used in the future if a person is following multiple Spots.

    Returns:
        A twiml Response or None.
    """
    # feeds = _LookupFollowedFeeds(from_number)
    resp = twiml.Response()
    resp.message(
        'Brendan is... dunno. The monkeys are still working on this feature.')
    return resp


def _RespondWeather(from_number, message):
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
    feed = _LookupOwnedFeed(from_number)
    resp = twiml.Response()
    if feed:
        resp.message("We'll get right on that sir *snicker*")
    else:
        resp.message("You're not Brendan, why do you care about the weather?")
    return resp


def _LookupOwnedFeed(number):
    """Return a feed (str) or None that the number is the owner of."""
    if number == config.BRENDAN_NUMBER:
        return 'feed'  # Put a real feed here.


def _LookupFollowedFeeds(number):
    """Return a list of feeds (str) that the given number is a follower of."""
    return []
