"""Model classes and frequently used functions for data access."""

from app.flask_app import db


"""
# Torn on whether to have a Feed model, or just limiting the app to one user.
class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.String, unique=True)
    nickname = db.Column(db.String)
"""


class Position(db.Model):

    """A GPS point for a given feed that may include additional info."""

    id = db.Column(db.Integer, primary_key=True)
    epoch = db.Column(db.Integer, unique=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    # Future thoughts:
    # If we go with a Feed model:
    # feed = db.Column(db.Integer, db.ForeignKey('Feed.id'))

    # Geo information:
    country = db.Column(db.Unicode)
    state = db.Column(db.Unicode)
    city = db.Column(db.Unicode)
    # I think there's more, see https://pypi.python.org/pypi/geolocation-python

    # Movement information:
    distance_from_prev = db.Column(db.Float)
    time_from_prev = db.Column(db.Float)
    speed_from_prev = db.Column(db.Float)

    # Weather information, although this might want to be elsewhere.
    # temperature = db.Column(db.Float)
    # apparent_temperature = db.Column(db.Float)  # "Feels like"
    # humidity = db.Column(db.Float)
    # weather_summary = db.Column(db.Float)
    # precip_probability = db.Column(db.Float)
    # precip_intensity = db.Column(db.Float)

    # I also want to start storing battery condition: string or enum?
    # that would be super helpful for alerting me that I need to charge.


class Post(db.Model):

    """A blog post."""

    id = db.Column(db.Integery, primary_key=True)

    # Wordpress stuff.
    post_id = db.Column(db.Integer, unique=True)
    status = db.Column(db.Unicode)
    title = db.Column(db.Unicode)
    content = db.Column(db.Unicode)
    timestamp = db.Column(db.Integer)
    link = db.Column(db.Unicode)
    location = db.Column(db.Unicode)

    # These may be real or may be synthetic based off GPS positions.
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)


_BRENDAN_FEED = '0Ya905pdnjgy0NflhOoL0GRDzLKUJn1nf'


def GetFeeds():
    """Return a list of tracked Spot feeds."""
    # Yup, we only care about Brendan.
    return [_BRENDAN_FEED]


def PositionRange(start=None, end=None):
    """Return a query object with optional start and end filters specified."""
    query = Position.query.filter()
    if start is not None:
        query = query.filter(Position.epoch >= start)
    if end is not None:
        query = query.filter(Position.epoch <= end)
    return query


def PositionAt(epoch):
    """Return a query object where the epoch matches."""
    return Position.query.filter(Position.epoch == epoch)


def GetLastPositions(count, before=None):
    """Return the last [count] points with epochs < before, if specified."""
    query = Position.query
    if before is not None:
        query = query.filter(Position.epoch < before)
    # Order by and limits must happen after any filters.
    return query.order_by(Position.epoch.desc()).limit(count)


def GetPositionsByIds(ids):
    """Return a query object by a list of position ids."""
    return Position.query.filter(Position.id.in_(ids))


def _IsField(name, only, skip):
    if only:
        return name in only
    invalid_fields = ['query', 'metadata', 'query_class'] + skip
    return name[0].islower() and name not in invalid_fields


def AsDict(obj, only=None, skip=None):
    """Return a dict of a row of data using attributes from the model class.

    Args:
        obj: The object to return as a dictionary.
        only: Optional list of fields that should be used in the dictionary.
        skip: Optional list of fields that should be skipped.
    """
    skip = list(skip) if skip else []
    return dict([
        (name, getattr(obj, name))
        for name in dir(obj.__class__) if _IsField(name, only, skip)])


def RowsAsDicts(rows, only=None, skip=None):
    """Return a list of dicts of data; see AsDict above."""
    return [AsDict(row, only=only, skip=skip) for row in rows]
