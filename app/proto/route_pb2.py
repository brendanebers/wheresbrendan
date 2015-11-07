# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: app/proto/route.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import app.proto.coordinate_pb2
import app.proto.duration_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='app/proto/route.proto',
  package='wheresbrendan',
  serialized_pb=_b('\n\x15\x61pp/proto/route.proto\x12\rwheresbrendan\x1a\x1a\x61pp/proto/coordinate.proto\x1a\x18\x61pp/proto/duration.proto\"\xc2\x01\n\x05Route\x12(\n\x05start\x18\x01 \x01(\x0b\x32\x19.wheresbrendan.Coordinate\x12&\n\x03\x65nd\x18\x02 \x01(\x0b\x32\x19.wheresbrendan.Coordinate\x12)\n\x08\x64uration\x18\x03 \x01(\x0b\x32\x17.wheresbrendan.Duration\x12,\n\twaypoints\x18\x04 \x03(\x0b\x32\x19.wheresbrendan.Coordinate\x12\x0e\n\x06\x66light\x18\x05 \x01(\x08')
  ,
  dependencies=[app.proto.coordinate_pb2.DESCRIPTOR,app.proto.duration_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_ROUTE = _descriptor.Descriptor(
  name='Route',
  full_name='wheresbrendan.Route',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='start', full_name='wheresbrendan.Route.start', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='end', full_name='wheresbrendan.Route.end', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='duration', full_name='wheresbrendan.Route.duration', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='waypoints', full_name='wheresbrendan.Route.waypoints', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='flight', full_name='wheresbrendan.Route.flight', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=95,
  serialized_end=289,
)

_ROUTE.fields_by_name['start'].message_type = app.proto.coordinate_pb2._COORDINATE
_ROUTE.fields_by_name['end'].message_type = app.proto.coordinate_pb2._COORDINATE
_ROUTE.fields_by_name['duration'].message_type = app.proto.duration_pb2._DURATION
_ROUTE.fields_by_name['waypoints'].message_type = app.proto.coordinate_pb2._COORDINATE
DESCRIPTOR.message_types_by_name['Route'] = _ROUTE

Route = _reflection.GeneratedProtocolMessageType('Route', (_message.Message,), dict(
  DESCRIPTOR = _ROUTE,
  __module__ = 'app.proto.route_pb2'
  # @@protoc_insertion_point(class_scope:wheresbrendan.Route)
  ))
_sym_db.RegisterMessage(Route)


# @@protoc_insertion_point(module_scope)
