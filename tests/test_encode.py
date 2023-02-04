import uuid

from encrypted_id import encode, decode
from django.test import TestCase


class TestEncode(TestCase):
    def test_encode_simple(self):
        sub_key = uuid.uuid4().hex
        assert decode(encode(10, sub_key), sub_key) == 10

    def test_encode(self):
        with self.settings(SECRET_KEY="34v*r6xdx^4o0_je66&yp48934&p77d3!dvy-8(s(ear3x1yvr"):
            assert encode(123, "abc") == "Rrh_U6BkP01CMZ3r1vYZZQ"
