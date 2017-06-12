import uuid

from encrypted_id import encode, decode


def test_encode():
    sub_key = uuid.uuid4().hex
    assert decode(encode(10, sub_key), sub_key) == 10
