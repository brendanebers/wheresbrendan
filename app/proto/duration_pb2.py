# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: app/proto/duration.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='app/proto/duration.proto',
  package='wheresbrendan',
  serialized_pb=_b('\n\x18\x61pp/proto/duration.proto\x12\rwheresbrendan\"0\n\x08\x44uration\x12\x12\n\nstart_time\x18\x01 \x01(\x02\x12\x10\n\x08\x65nd_time\x18\x02 \x01(\x02')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_DURATION = _descriptor.Descriptor(
  name='Duration',
  full_name='wheresbrendan.Duration',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='start_time', full_name='wheresbrendan.Duration.start_time', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='end_time', full_name='wheresbrendan.Duration.end_time', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=43,
  serialized_end=91,
)

DESCRIPTOR.message_types_by_name['Duration'] = _DURATION

Duration = _reflection.GeneratedProtocolMessageType('Duration', (_message.Message,), dict(
  DESCRIPTOR = _DURATION,
  __module__ = 'app.proto.duration_pb2'
  # @@protoc_insertion_point(class_scope:wheresbrendan.Duration)
  ))
_sym_db.RegisterMessage(Duration)


# @@protoc_insertion_point(module_scope)