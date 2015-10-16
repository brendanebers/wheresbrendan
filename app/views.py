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
@app.route('/blog')
@app.route('/blog/<post_id>')
@app.route('/blog/<post_id>/<post_title>')
def Index(*args, **kwargs):
    """Return the index page."""
    return app.send_static_file('index.html')


@app.route('/images/<filename>')
def Images(filename):
    return app.send_static_file(os.path.join('images', filename))


@app.route('/refresh')
def Refresh():
    """Temporary, syncronous method for getting spot data."""
    print 'View call to store new spot data'
    spot.StoreNewData()
    return 'success!'


def _MakeEpoch(val, default, supplement=False):
    if not val:
        return default
    elif isinstance(val, (int, float)):
        return val
    elif isinstance(val, (str, unicode)):
        if val.isdigit():
            return int(val)
        dt = parser.parse(val)
        # DT to epoch conversion from: http://stackoverflow.com/a/11111177
        nineteen_seventy = datetime.datetime.utcfromtimestamp(0)
        delta = dt - nineteen_seventy
        epoch = delta.total_seconds()
        if supplement:
            # We add a day+. This is cheating, but the UI mostly supports dates,
            # and I'd rather the date be inclusive. The "+" is for timezones.
            print 'supplemented!'
            epoch += 30*60*60
        return epoch
    return default


@app.route('/api/history.json')
def GetHistory():
    """Return positions and posts within specified time range."""
    start = _MakeEpoch(request.args.get('start'), 0)
    end = _MakeEpoch(request.args.get('end'), 999999999999, supplement=True)
    history = combined_model.Range(start=start, end=end)
    return json.dumps({'points': history})


@app.route('/api/current.json')
def Current():
    """Return the current location information."""
    position_rows = position_model.GetLastPositions(1)
    position = utils.RowsAsDicts(position_rows)[0]
    position['elapsed'] = int(now.Now() - position['epoch'])
    position['elapsed_humanized'] = now.HumanizeSeconds(position['elapsed'])
    return json.dumps(position)


@app.route('/api/post.json')
def GetPost():
    """Get a specific post."""
    our_id = int(request.values.get('id'))
    post = post_model.GetPostDict(our_id, private=False)
    return json.dumps(post)


@app.route('/api/post_list.json')
def GetPostList():
    """Get a list of post titles, URLs, IDs and epochs."""
    # TODO: Pagination and date/time ranges.
    posts = post_model.GetPostDictList(private=False)
    return json.dumps(sorted(posts, key=lambda p: p['epoch'], reverse=True))


@app.route('/api/wordpress/')
def NewWordpress():
    """Update local records of wordpress articles."""
    post_id = str(request.values.get('id'))
    celery_app.send_task('app.tasks.wordpress.UpdatePost', [post_id])
    return 'added to the processing queue'
