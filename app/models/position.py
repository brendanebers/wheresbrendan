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
    temperature = db.Column(db.Float)
    apparent_temperature = db.Column(db.Float)  # "Feels like"
    humidity = db.Column(db.Float)
    precip_probability = db.Column(db.Float)
    precip_intensity = db.Column(db.Float)
    weather_summary = db.Column(db.Unicode)
    precip_type = db.Column(db.Unicode)
    wind_speed = db.Column(db.Unicode)

    # I also want to start storing battery condition: string or enum?
    # that would be super helpful for alerting me that I need to charge.


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


def SavePositions(positions):
    """Save new positions to database."""
    for position in positions:
        db.session.add(position)
    db.session.commit()


def UpdatePositions(positions):
    """Commit changes to updated positions."""
    db.session.commit()
