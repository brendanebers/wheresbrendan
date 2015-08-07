"""Functions and tools for interfacing with wordpress blog."""

# It might be possible to write a wordpress plugin that'll make a simple post
# to our API when a page is changed...
# https://codex.wordpress.org/Plugin_API/Action_Reference/save_post

import datetime
import wordpress_xmlrpc  # https://python-wordpress-xmlrpc.readthedocs.org
from wordpress_xmlrpc.methods import posts as wp_posts

import config
from app import now
from app.models import post as post_model
from app.models import position as position_model


def _Client():
    return wordpress_xmlrpc.Client(
        config.WORDPRESS_SITE, config.WORDPRESS_USER, config.WORDPRESS_PASSWORD)


def _ToEpoch(dt):
    """Return epoch from wordpress's peculiar DateTime object."""
    tt = dt.timetuple()
    return datetime.datetime(
        year=tt.tm_year, month=tt.tm_mon, day=tt.tm_mday, hour=tt.tm_hour,
        minute=tt.tm_min, second=tt.tm_sec)


def _ExtractLocation(struct):
    location = ''
    latitude, longitude = None, None
    for field in struct.get('custom_fields', []):
        if field.get('key') == 'geo_address':
            location = field.get('value')
        if field.get('key') == 'geo_latitude':
            latitude = field.get('value')
        if field.get('key') == 'geo_longitude':
            longitude = field.get('value')
    return location, latitude, longitude


def _ToPostModel(post):
    post_dt = _ToEpoch(post.struct['post_date_gmt'])
    post_ts = now.DtToEpoch(post_dt)
    loc, lat, lng = _ExtractLocation(post.struct)
    kwargs = dict(
        post_id=post.id, title=post.title, content=post.content, link=post.link,
        status=post.struct.get('post_status'), epoch=post_ts)
    if all([loc, lat, lng]):
        kwargs.update(dict(location=loc, latitude=lat, longitude=lng))
    return post_model.Post(**kwargs)


def GetPosts(count=100):
    """Return public wordpress posts."""
    client = _Client()
    post_query = wp_posts.GetPosts({'post_status': 'publish', 'number': count})
    posts = client.call(post_query)
    return posts


def GetPost(post_id):
    """Return a given post by ID."""
    client = _Client()
    post_query = wp_posts.GetPosts({'post_id': post_id})
    posts = client.call(post_query)
    return posts[0] if posts else None


def UpdatePosts():
    """Ensure all posts in the database are up to date."""
    posts = GetPosts()
    posts = [_ToPostModel(post) for post in posts]
    post_model.SavePosts(posts)


def UpdatePost(post_id):
    """Ensure given post id is up to date in the database."""
    post = GetPost(post_id)
    post = _ToPostModel(post)
    post_model.SavePosts([post])


def AddPosition(post):
    """Add latitude and longitude to the given post."""
    # This is a cheat, and expects the previous location to be "good enough"
    position = position_model.GetLastPositions(1, before=post.epoch).first()
    if position:
        post.latitude = position.latitude
        post.longitude = position.longitude
        post_model.UpdatePosts([post])
    else:
        print 'No position could be found before the given post.'
