""""Module for combining model data to present to the view."""

from app.models import position as position_model
from app.models import post as post_model
from app.models import utils


def TagShortStops(positions):
    """Tag short stops with ['icon'] = 'position'."""
    previous = None
    for position in positions:
        if not previous:
            previous = position
            continue

        # This is a cheat, we need to use tags that I'm not saving yet.
        if (position['epoch'] - previous['epoch']) > 60*60:  # More than an hour
            previous = position
            continue

        previous['icon'] = 'position'
        previous = position


def Range(start=None, end=None):
    """Return combined position and post dictionaries for given range."""
    positions = position_model.PositionRange(start=start, end=end)
    positions = utils.RowsAsDicts(positions)
    positions.sort(key=lambda p: p['epoch'])
    TagShortStops(positions)
    # TODO: Update skip fields

    posts = post_model.PostRange(start=start, end=end)
    # TODO: Update skip fields
    posts = utils.RowsAsDicts(posts, skip=['content'])
    for post in posts:
        post['icon'] = 'wordpress'

    combined = positions + posts
    combined.sort(key=lambda p: p['epoch'])
    return combined
