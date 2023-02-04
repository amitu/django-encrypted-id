import pytest
from encrypted_id import EncryptedIDDecodeError, decode, encode
from django.test import TestCase


class TestDecode(TestCase):
    def test_decode(self):
        with self.settings(SECRET_KEY="34v*r6xdx^4o0_je66&yp48934&p77d3!dvy-8(s(ear3x1yvr"):
            assert decode("Rrh_U6BkP01CMZ3r1vYZZQ", "abc") == 123

    def test_decode_error_empty_input(self):
        with pytest.raises(EncryptedIDDecodeError):
            decode("", "")  # strucr.error

    def test_decode_error_empty_sub_key(self):
        with pytest.raises(EncryptedIDDecodeError):
            decode("1", "")  # binascii.Error

    def test_decode_error_wrong_ekey(self):
        with pytest.raises(EncryptedIDDecodeError):
            decode(encode(0, "")[:-1] + 'Z', "")  # crc error
