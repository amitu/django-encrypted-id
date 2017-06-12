import pytest

from encrypted_id import EncryptedIDDecodeError, decode, encode


def test_decode():
    with pytest.raises(EncryptedIDDecodeError):
        decode("", "")                                      # strucr.error
    with pytest.raises(EncryptedIDDecodeError):
        decode("1", "")                                     # binascii.Error
    with pytest.raises(EncryptedIDDecodeError):
        decode(encode(0, "")[:-1] + 'Z', "")                # crc error