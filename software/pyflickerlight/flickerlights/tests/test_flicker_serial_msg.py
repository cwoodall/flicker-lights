from ..proto import *

def test_encode_message():
    assert(encode_message(b"\x00\x01") == b"\x7D\x00\x01\x7D")
