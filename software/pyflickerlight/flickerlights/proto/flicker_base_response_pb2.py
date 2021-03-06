# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flicker_base_response.proto

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
  name='flicker_base_response.proto',
  package='',
  serialized_pb=_b('\n\x1b\x66licker_base_response.proto\"\x83\x01\n\x13\x46lickerBaseResponse\x12+\n\x03\x65rr\x18\x01 \x02(\x0e\x32\x1e.FlickerBaseResponse.ErrorType\"?\n\tErrorType\x12\x07\n\x03\x41\x43K\x10\x00\x12\x10\n\x0c\x44\x45\x43ODE_ERROR\x10\x01\x12\x17\n\x13\x43OMMUNICATION_ERROR\x10\x02')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_FLICKERBASERESPONSE_ERRORTYPE = _descriptor.EnumDescriptor(
  name='ErrorType',
  full_name='FlickerBaseResponse.ErrorType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ACK', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DECODE_ERROR', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='COMMUNICATION_ERROR', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=100,
  serialized_end=163,
)
_sym_db.RegisterEnumDescriptor(_FLICKERBASERESPONSE_ERRORTYPE)


_FLICKERBASERESPONSE = _descriptor.Descriptor(
  name='FlickerBaseResponse',
  full_name='FlickerBaseResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='err', full_name='FlickerBaseResponse.err', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _FLICKERBASERESPONSE_ERRORTYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=32,
  serialized_end=163,
)

_FLICKERBASERESPONSE.fields_by_name['err'].enum_type = _FLICKERBASERESPONSE_ERRORTYPE
_FLICKERBASERESPONSE_ERRORTYPE.containing_type = _FLICKERBASERESPONSE
DESCRIPTOR.message_types_by_name['FlickerBaseResponse'] = _FLICKERBASERESPONSE

FlickerBaseResponse = _reflection.GeneratedProtocolMessageType('FlickerBaseResponse', (_message.Message,), dict(
  DESCRIPTOR = _FLICKERBASERESPONSE,
  __module__ = 'flicker_base_response_pb2'
  # @@protoc_insertion_point(class_scope:FlickerBaseResponse)
  ))
_sym_db.RegisterMessage(FlickerBaseResponse)


# @@protoc_insertion_point(module_scope)
