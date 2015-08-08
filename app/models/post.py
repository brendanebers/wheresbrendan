"""Post model and related functions."""

from app.flask_app import db
from app.models import utils


class Post(db.Model):

    """A blog post."""

    id = db.Column(db.Integer, primary_key=True)

    # Wordpress stuff.
    post_id = db.Column(db.Integer, unique=True)
    status = db.Column(db.Unicode)
    title = db.Column(db.Unicode)
    content = db.Column(db.Unicode)
    epoch = db.Column(db.Integer)
    link = db.Column(db.Unicode)
    location = db.Column(db.Unicode)

    # These may be real or may be synthetic based off GPS positions.
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)


def PostRange(start=None, end=None, private=False):
    """Return a query object with optional start and end filters specified."""
    query = Post.query.filter()
    if not private:
        query = Post.query.filter(Post.status == 'publish')
    if start is not None:
        query = query.filter(Post.epoch >= start)
    if end is not None:
        query = query.filter(Post.epoch <= end)
    return query


def GetPost(our_id, private=False):
    """Return a Post query by our id."""
    query = Post.query.filter(Post.id == our_id)
    if not private:
        query = query.filter(Post.status == 'publish')
    return query


def GetPostDict(our_id, private=False):
    """Return a Post dictionary by our id."""
    query = GetPost(our_id, private=private)
    post = query.first()
    if not post:
        return None
    post_dict = utils.AsDict(post)
    content = post_dict['content']
    post_dict['content'] = '<p>' + content.replace('\n\n', '</p><p>') + '</p>'
    return post_dict


def SavePosts(posts):
    """Save new posts and update existing posts."""
    old_posts = {}
    for post in posts:
        old = Post.query.filter(Post.post_id == post.post_id).first()
        if old:
            old_posts[post.post_id] = old

    for post in posts:
        if post.post_id not in old_posts:
            db.session.add(post)
        else:
            old = old_posts[post.post_id]
            old.post_id = post.post_id
            old.status = post.status
            old.title = post.title
            old.content = post.content
            old.epoch = post.epoch
            old.link = post.link
            old.location = post.location
            old.latitude = post.latitude
            old.longitude = post.longitude
            old.private = post.private
    db.session.commit()


def UpdatePosts(posts):
    """Commit changes to updated posts."""
    db.session.commit()
