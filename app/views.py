import datetime
from dateutil import parser
import flask
from flask import request
import json

import config
from app.flask_app import flask_app as app
from app import models
from app import texting


@app.route('/')
@app.route('/index')
def index():
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
    start = _MakeEpoch(request.args.get('start'), 0)
    end = _MakeEpoch(request.args.get('end'), 999999999999)
    positions = models.PositionRange(start=start, end=end)
    return json.dumps(
        {'points': models.RowsAsDicts(positions, skip=['date_recorded'])})


@app.route('/api/texting/', methods=['GET', 'POST'])
def handle_texts():
    resp = texting.HandleIncoming(
        request.values.get('From'), request.values.get('Body'))
    return str(resp)
