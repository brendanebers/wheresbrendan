"""Module for reading/writing Route data."""

from app.models import redis_shared
from app.proto import route_pb2


def Set(route_pb):
    key = 'route-' + redis_shared.ProtoId(route_pb)
    client = redis_shared.Client()
    client.set(key, route_pb.SerializeToString())


def GetAll():
    """Returns all route protos."""
    client = redis_shared.Client()
    for key in client.scan_iter():
        if key.startswith('route'):
            route_str = client.get(key)
            yield route_pb2.Route.FromString(route_str)


def Get(route_id):
    """Get a specific route by id."""
    return redis_shared.Client().get('route-' + route_id)
