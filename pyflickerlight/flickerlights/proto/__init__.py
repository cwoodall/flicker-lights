from .flicker_base_message_pb2 import *
from .flicker_base_response_pb2 import *

import logging
logger = logging.getLogger(__name__)

def encode_message(msg, msg_delimiter=b'\x7D', escape_char=b'\x7E'):
    final_msg = msg_delimiter
    for b in msg:
        if b in [msg_delimiter, escape_char]:
            logger.debug(b)
            final_msg += escape_char
        final_msg += bytes([b])
    final_msg += msg_delimiter
    logger.debug(final_msg)
    return final_msg

class FlickerSerialMsg(object):
    def __init__(self, payload, msg_delimiter=b'\x7D', escape_char=b'\x7E'):
        self.__msg_delimiter = msg_delimiter
        self.__escape_char = escape_char
        self.payload = payload

        if type(payload) == bytes:
            self.payload_type = "bytes"
        elif getattr(payload, "SerializeToString", None):
            self.payload_type = "SerializeToString"
        elif getattr(payload, "serialize", None):
            self.payload_type = "serialize"
        else:
            raise Exception("Please provide a serializable type")

    def serialize(self):
        serialized_payload = b""
        if self.payload_type == "bytes":
            serialized_payload = self.payload
        elif self.payload_type == "SerializeToString":
            serialized_payload = self.payload.SerializeToString()
        elif self.payload_type == "serialize":
            serialized_payload = self.payload.serialize()
        else:
            raise Exception("Invalid payload type {}".format(self.payload_type))

        return encode_message(serialized_payload)
