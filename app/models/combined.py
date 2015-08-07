""""Module for combining model data to present to the view."""

from app.models import position as position_model
from app.models import post as post_model
from app.models import utils


def Range(start=None, end=None):
    """Return combined position and post dictionaries for given range."""
    positions = position_model.PositionRange(start=start, end=end)
    positions = utils.RowsAsDicts(positions)  # TODO: Update skip fields
    # TODO: Positions that are just movement should be a little icon.

    posts = post_model.PostRange(start=start, end=end)
    # TODO: Update skip fields
    posts = utils.RowsAsDicts(posts, skip=['content'])
    for post in posts:
        post['icon'] = 'wordpress'

    combined = positions + posts
    combined.sort(key=lambda p: p['epoch'])
    return combined
