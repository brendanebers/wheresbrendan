"""Module for reading/writing Stop data."""

from app.models import redis_shared
from app.proto import stop_pb2


def Set(stop_pb):
    key = 'stop-' + redis_shared.ProtoId(stop_pb)
    client = redis_shared.Client()
    client.set(key, stop_pb.SerializeToString())


def GetAll():
    """Returns all stop protos."""
    client = redis_shared.Client()
    for key in client.scan_iter():
        if key.startswith('stop'):
            stop_str = client.get(key)
            yield stop_pb2.Stop.FromString(stop_str)


def Get(stop_id):
    """Get a specific stop by id."""
    return redis_shared.Client().get('stop-' + stop_id)
