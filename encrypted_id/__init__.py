import base64
import binascii
import hashlib
import struct

from Cryptodome.Cipher import AES
from django.conf import settings
from django.db.models import Model
from django.http import Http404
from django.shortcuts import get_object_or_404 as go4


class EncryptedIDDecodeError(Exception):
    def __init__(self, msg="Failed to decrypt, invalid input."):
        super(EncryptedIDDecodeError, self).__init__(msg)


def encode(the_id, sub_key):
    assert 0 <= the_id < 2 ** 64

    version = 1

    crc = binascii.crc32(str(the_id).encode("utf-8")) & 0xffffffff

    message = struct.pack(b"<IQI", crc, the_id, version)
    assert len(message) == 16

    key = settings.SECRET_KEY
    iv = hashlib.sha256((key + sub_key).encode("ascii")).digest()[:16]
    cypher = AES.new(key[:32].encode("utf-8"), AES.MODE_CBC, iv)

    eid = base64.urlsafe_b64encode(cypher.encrypt(message)).replace(b"=", b"")
    return eid.decode("utf-8")


def decode(e, sub_key):
    if isinstance(e, str):
        e = bytes(e.encode("ascii"))

    try:
        padding = (3 - len(e) % 3) * b"="
        e = base64.urlsafe_b64decode(e + padding)
    except (TypeError, AttributeError, binascii.Error):
        raise EncryptedIDDecodeError()

    for key in getattr(settings, "SECRET_KEYS", [settings.SECRET_KEY]):
        iv = hashlib.sha256((key + sub_key).encode("ascii")).digest()[:16]
        cypher = AES.new(key[:32].encode("utf-8"), AES.MODE_CBC, iv)
        try:
            msg = cypher.decrypt(e)
        except ValueError:
            raise EncryptedIDDecodeError()

        try:
            crc, the_id, _ = struct.unpack(b"<IQI", msg)
        except struct.error:
            raise EncryptedIDDecodeError()

        try:
            id_str = str(the_id).encode("utf-8")
            expected_crc = binascii.crc32(id_str) & 0xffffffff
        except (MemoryError, OverflowError):
            raise EncryptedIDDecodeError()

        if crc != expected_crc:
            continue

        return the_id
    raise EncryptedIDDecodeError("Failed to decrypt, CRC never matched.")


def get_model_sub_key(model: Model):
    try:
        return model._meta.ek_key
    except AttributeError:
        return model._meta.db_table


def get_object_or_404(model: Model, ekey: str, *arg, **kwargs):
    try:
        pk = decode(ekey, get_model_sub_key(model))
    except EncryptedIDDecodeError:
        raise Http404

    return go4(model, id=pk, *arg, **kwargs)


def ekey(instance: Model):
    assert isinstance(instance, Model)
    return encode(instance.id, get_model_sub_key(instance))
