"""Views for wheresbrendan application."""

import datetime
from dateutil import parser
from flask import request
import json
import os

from app.flask_app import flask_app as app
from app import now
from app.models import combined as combined_model
from app.models import position as position_model
from app.models import post as post_model
from app.models import utils
from app.tasks.celery_app import celery_app

# Delete once we're back to asyncronous
from app.tasks import spot


@app.route('/')
@app.route('/now')
@app.route('/history')
@app.route('/history/<start_date>/to/<end_date>')
def Index(*args, **kwargs):
    """Return the index page."""
    return app.send_static_file('index.html')


@app.route('/images/<filename>')
def Images(filename):
    return app.send_static_file(os.path.join('images', filename))


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
def GetPositions():
    """Return positions within specified time range."""
    start = _MakeEpoch(request.args.get('start'), 0)
    end = _MakeEpoch(request.args.get('end'), 999999999999)
    positions = position_model.PositionRange(start=start, end=end)
    return json.dumps(
        {'points': utils.RowsAsDicts(positions, skip=['date_recorded'])})


@app.route('/api/history/')
def GetHistory():
    """Return positions and posts within specified time range."""
    start = _MakeEpoch(request.args.get('start'), 0)
    end = _MakeEpoch(request.args.get('end'), 999999999999)
    history = combined_model.Range(start=start, end=end)
    return json.dumps({'points': history})


@app.route('/api/current/')
def Current():
    """Return the current location information."""
    position_rows = position_model.GetLastPositions(1)
    position = utils.RowsAsDicts(position_rows)[0]
    position['elapsed'] = int(now.Now() - position['epoch'])
    position['elapsed_humanized'] = now.HumanizeSeconds(position['elapsed'])
    return json.dumps(position)


@app.route('/api/spot_fetch/')
def TemporarySpotFetch():
    """Temporary, syncronous method for getting spot data."""
    print 'View call to store new spot data'
    spot.StoreNewData()
    return 'success!'


@app.route('/api/wordpress/')
def NewWordpress():
    """Update local records of wordpress articles."""
    post_id = str(request.values.get('id'))
    celery_app.send_task('app.tasks.wordpress.UpdatePost', [post_id])
    return 'added to the processing queue'


@app.route('/api/post/')
def GetPost():
    """Get a specific post."""
    our_id = str(request.values.get('id'))
    post = post_model.GetPostDict(our_id, private=False)
    return json.dumps(post)
