"""Functions and tools for interfacing with wordpress blog."""

# It might be possible to write a wordpress plugin that'll make a simple post
# to our API when a page is changed...
# https://codex.wordpress.org/Plugin_API/Action_Reference/save_post

# https://python-wordpress-xmlrpc.readthedocs.org
import wordpress_xmlrpc
from wordpress_xmlrpc.methods import posts as wp_posts

import config


def _Client():
    return wordpress_xmlrpc.Client(
        config.WORDPRESS_SITE, config.WORDPRESS_USER, config.WORDPRESS_PASSWORD)


def GetPosts():
    """Return public wordpress posts."""
    client = _Client()
    post_query = wp_posts.GetPosts({'post_status': 'publish'})
    posts = client.call(post_query)
    return posts
