"""Views for wheresbrendan application."""

import datetime
from dateutil import parser
from flask import request
import json

from app.flask_app import flask_app as app
from app import models


@app.route('/')
@app.route('/index')
@app.route('/then')
@app.route('/now')
def index():
    """Return the index page."""
    return app.send_static_file('index.html')


def _MakeEpoch(val, default):
    if not val:
        return default
    elif isinstance(val, (int, float)):
        return val
    elif isinstance(val, (str, unicode)):
        if val.isdigit():
            return int(val)
        dt = parser.parse(val)
        # DT to epoch conversion from: http://stackoverflow.com/a/11111177
        epoch = datetime.datetime.utcfromtimestamp(0)
        delta = dt - epoch
        return delta.total_seconds()
    return default


@app.route('/api/get_positions/')
def get_positions():
    """Return positions within specified time range."""
    start = _MakeEpoch(request.args.get('start'), 0)
    end = _MakeEpoch(request.args.get('end'), 999999999999)
    positions = models.PositionRange(start=start, end=end)
    return json.dumps(
        {'points': models.RowsAsDicts(positions, skip=['date_recorded'])})
