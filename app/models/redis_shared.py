import redis
import uuid

import config


def Client():
    return redis.from_url(config.REDIS_URL)


def ProtoId(obj_pb):
    """Returns a proto objects id, setting an id if it does not exist."""
    if hasattr(obj_pb, 'id') and getattr(obj_pb, 'id'):
        return obj_pb.id
    obj_pb.id = str(uuid.uuid4).split('-', 1)[0]
    return obj_pb.id
