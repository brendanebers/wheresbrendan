import gpxdata

from app import now
from app.models import position as model
from app.tasks import spot as spot_tasks


def ParseGPX(gpx_file):
    print 'Parsing GPX file'
    gpx = gpxdata.Document.readGPX(gpx_file)
    positions = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                positions.append(model.Position(
                    epoch=now.DtToEpoch(point.t), latitude=point.lat,
                    longitude=point.lon))
    print 'Parsed %d positions from GPX file' % len(positions)
    return positions


def HandleGPXFile(gpx_file):
    print 'Handling new GPX file'
    positions = ParseGPX(gpx_file)
    positions = [p for p in positions if not model.PositionAt(p.epoch).count()]
    if positions:
        print 'Saving %d new points from GPX file' % (len(positions))
        model.SavePositions(positions)
        spot_tasks.PostFetch(positions)
    else:
        print 'No new points to save from GPX file'
