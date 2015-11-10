from app.models import position as position_db
from app.proto import coordinate_pb2
from app.proto import route_pb2
from app.proto import stop_pb2
from app.tasks import basic_geo


# Goal: find all stays from huge gaps in duration
# Merge stays that are within 5 km of each other into a stop
#
# Also: find all "stays" where the movement was minimal for > 1 hour
# let's merge them if they're within 2 km of each other.
#
# And some moving stays butt into duration stays, either arriving or departing.


def PositionsToStops(positions=None):
    if not positions:
        positions = position_db.PositionRange()  # Query object
        positions = list(positions)  # Indexable
    positions = sorted(positions, key=lambda p: p.epoch)
    print 'Finding stops from %d positions' % len(positions)

    duration_stays = FindDurationStays(positions)
    print 'Found %d duration stays' % len(duration_stays)
    moving_stays = FindMovingStays(positions)
    print 'Found %d moving stays' % len(moving_stays)

    combined_stays = duration_stays + moving_stays
    print 'Looking for stops in %d total stays' % len(combined_stays)

    stops = []
    # n^2 operation to find all stops within 5km proximity
    for stay, loc in combined_stays:
        for stop in stops:
            distance = basic_geo.ConvenientDistance(loc, stop.location)
            if distance <= 5000:
                print 'Stop combined!'
                stop.stays.extend([stay])
                break
        else:
            stop = stop_pb2.Stop()
            stop.location.latitude = loc.latitude
            stop.location.longitude = loc.longitude
            stop.stays.extend([stay])
            stops.append(stop)

    print 'Found %d stops' % len(stops)
    return stops


def FindDurationStays(positions):
    stays = []
    stay, loc = StayLocTuple(positions[0], positions[0])
    stays.append((stay, loc))

    prev = positions[0]
    for position in positions[1:]:
        if (position.epoch - prev.epoch) > 60*60:
            stay, loc = StayLocTuple(prev, position)
            stays.append((stay, loc))
        prev = position
    return stays


def StayLocTuple(start, end):
    stay = stop_pb2.Stay()
    stay.duration.start_time = start.epoch
    stay.duration.end_time = end.epoch

    loc = coordinate_pb2.Coordinate()
    loc.latitude = start.latitude
    loc.longitude = start.longitude
    return (stay, loc)


def FindMovingStays(positions):
    # When there's less than 5km movement in over an hour
    stays = []
    start = positions[0]
    last = positions[0]
    for position in positions:
        distance = basic_geo.ConvenientDistance(start, position)
        delta_t = position.epoch - last.epoch
        # Slow movement requires distance and less than ~30 minutes (33 for 10%)
        # between readings
        if distance < 5000 and delta_t <= 60*33:
            last = position
        else:
            if last.epoch - start.epoch >= 60*60:  # Did we have one?
                stay, loc = StayLocTuple(start, last)
                stays.append((stay, loc))
            start = last = position  # reset!

    return stays


# Temporary method, lets fabricate routes based on stops.
def RoutesFromStops(stops):
    stays = StaysToStops(stops)
    _, start_stay, start_loc = stays[0]
    for _, end_stay, end_loc in stays[1:]:
        route = route_pb2.Route()

        route.start.latitude = start_loc.latitude
        route.start.longitude = start_loc.longitude
        route.duration.start_time = start_stay.duration.end_time

        route.end.latitude = end_loc.latitude
        route.end.longitude = end_loc.longitude
        route.duration.end_time = end_stay.duration.start_time

        start_stay = end_stay
        start_loc = end_loc


def StaysToStops(stops):
    """Return a list of (time, stay, stop) tuples sorted by stay start time."""
    results = []
    for stop in stops:
        for stay in stop.stays:
            results.append((stay.duration.start_time, stay, stop))
    return sorted(results, lambda tup: tup[0])
