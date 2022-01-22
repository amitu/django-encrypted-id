import uuid

from encrypted_id import encode, decode
from django.test import TestCase


class TestEncode(TestCase):
    def test_encode(self):
        sub_key = uuid.uuid4().hex
        assert decode(encode(10, sub_key), sub_key) == 10
