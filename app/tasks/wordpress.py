"""Functions and tools for interfacing with wordpress blog."""

# It might be possible to write a wordpress plugin that'll make a simple post
# to our API when a page is changed...
# https://codex.wordpress.org/Plugin_API/Action_Reference/save_post

import datetime
import wordpress_xmlrpc  # https://python-wordpress-xmlrpc.readthedocs.org
from wordpress_xmlrpc.methods import posts as wp_posts

import config
from app import models


def _Client():
    return wordpress_xmlrpc.Client(
        config.WORDPRESS_SITE, config.WORDPRESS_USER, config.WORDPRESS_PASSWORD)


def _ToEpoch(dt):
    """Return epoch from wordpress's peculiar DateTime object."""
    tt = dt.timetuple()
    return datetime.datetime(
        year=tt.tm_year, month=tt.tm_mon, day=tt.tm_mday, hour=tt.tm_hour,
        minute=tt.tm_min, second=tt.tm_sec)


def _ToPostModel(post):
    post_ts = _ToEpoch(post.struct['post_date_gmt'])
    return models.Post(
        post_id=post.id, title=post.title, status=post.status,
        content=post.content, link=post.link, timestamp=post_ts)


def GetPosts():
    """Return public wordpress posts."""
    client = _Client()
    post_query = wp_posts.GetPosts({'post_status': 'publish'})
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


def UpdatePost(post_id):
    """Ensure given post id is up to date in the database."""
    post = GetPost(post_id)
    post = _ToPostModel(post)
