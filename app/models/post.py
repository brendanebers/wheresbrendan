"""Post model and related functions."""

from app.flask_app import db


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
            old.timestamp = post.timestamp
            old.link = post.link
            old.location = post.location
            old.latitude = post.latitude
            old.longitude = post.longitude
    db.session.commit()


def UpdatePosts(posts):
    """Commit changes to updated posts."""
    db.session.commit()
