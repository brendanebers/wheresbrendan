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


def HandleIncoming(from_number, original_message):
    """Routes an incoming text message."""
    lowered = original_message.lower().split(None, 1)
    if not lowered:
        return None
    command = lowered[0]
    message = lowered[1] if len(lowered) == 2 else ''

    if command.startswith('weather'):
        return _RespondWeather(from_number, message)

    # We'll try to tell them where anyways...
    elif command.startswith('where') or True:
        return _RespondWhere(from_number, message)


def _RespondWhere(from_number, message):
    """Responds where a tracked spot is.

    args:
        from_number: The number that sent the request.
        message: The message, stripped of the command. Initially ignored, but
            could be used in the future if a person is following multiple Spots.
    """
    feeds = _LookupFollowedFeeds(from_number)
    resp = twilio.twiml.Response()
    resp.message(
        'Brendan is... dunno. The monkeys are still working on this feature.')
    return resp


def _RespondWeather(from_number, message):
    """Responds with weather info of current location, destination, or between.

    This method responds asynchronously to valid requests.

    args:
        from_number: The number that sent the request, should correspond with a
            tracked Spot.
        message: The message, stripped of the "weather" command. If empty, the
            weather at current location will be sent. If the message is just
            location, like "Mexico city", then the weather at Mexico City will
            be sent. If the message is "to Mexico City", then a temp range and
            chance of rain between current location and Mexico City will be
            sent.
    """
    feed = _LookupOwnedFeed(from_number)
    resp = twilio.twiml.Response()
    if feed:
        resp.message("We'll get right on that sir *snicker*")
    else:
        resp.message("You're not Brendan, why do you care about the weather?")
    return resp


def _LookupOwnedFeed(number):
    """Returns a feed (str) or None that the number is the owner of."""
    if number == config.BRENDAN_NUMBER:
        return 'feed'


def _LookupFollowedFeeds(number):
    """Returns a list of feeds (str) that the given number is a follower of."""
    return []


_COMMANDS = {'where': _RespondWhere, 'weather', _RespondWeather}
