""""Module for combining model data to present to the view."""

import collections

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


def _GetPosts(start, end):
    """Get posts for combined data."""
    posts = post_model.PostRange(start=start, end=end)

    # TODO: Update skip fields
    posts = utils.RowsAsDicts(posts, skip=['content'])

    posts = _CombinePosts(posts)
    _AddPostTitles(posts)
    return posts


def _CombinePosts(posts):
    """Combine posts together."""
    points = collections.defaultdict(list)
    for post in posts:
        coord = (post.pop('latitude'), post.pop('longitude'))
        points[coord].append(post)
    print points

    results = []
    for coord, posts in points.iteritems():
        print 'just combined %d posts' % len(posts)
        results.append(dict(latitude=coord[0], longitude=coord[1], posts=posts,
                            epoch=posts[0]['epoch'], icon='wordpress'))
    return results


def _AddPostTitles(posts):
    """Adds a title attribute to posts."""
    for post in posts:
        if len(post['posts']) > 1:
            post['title'] = '%d blog entries' % len(post['posts'])
        else:
            post['title'] = post['posts'][0]['title']


def _FilterPositions(positions, posts):
    post_coords = set((p['latitude'], p['longitude']) for p in posts)
    for p in positions:
        if (p['latitude'], p['longitude']) not in post_coords:
            yield p


def Range(start=None, end=None):
    """Return combined position and post dictionaries for given range."""
    positions = position_model.PositionRange(start=start, end=end)
    positions = utils.RowsAsDicts(positions)
    positions.sort(key=lambda p: p['epoch'])
    TagShortStops(positions)
    # TODO: Update skip fields

    posts = _GetPosts(start, end)
    positions = list(_FilterPositions(positions, posts))
    combined = positions + posts
    combined.sort(key=lambda p: p['epoch'])
    return combined
