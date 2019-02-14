# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

try:
    basestring
except NameError:
    basestring = str

from Crypto.Cipher import AES

import base64
import binascii
import hashlib
import struct

from django.conf import settings
from django.db.models import Model
from django.http import Http404
from django.shortcuts import get_object_or_404 as go4


__version__ = "0.3.2"
__license__ = "BSD"
__author__ = "Amit Upadhyay"
__email__ = "upadhyay@gmail.com"
__url__ = "http://amitu.com/encrypted-id/"
__source__ = "https://github.com/amitu/django-encrypted-id"
__docformat__ = "html"


class EncryptedIDDecodeError(Exception):
    def __init__(self, msg="Failed to decrypt, invalid input."):
        super(EncryptedIDDecodeError, self).__init__(msg)


def encode(the_id, sub_key):
    assert 0 <= the_id < 2 ** 64

    version = 1

    crc = binascii.crc32(str(the_id).encode('utf-8')) & 0xffffffff

    message = struct.pack(b"<IQI", crc, the_id, version)
    assert len(message) == 16

    key = settings.SECRET_KEY
    iv = hashlib.sha256((key + sub_key).encode('ascii')).digest()[:16]
    cypher = AES.new(key[:32].encode('utf-8'), AES.MODE_CBC, iv)

    eid = base64.urlsafe_b64encode(cypher.encrypt(message)).replace(b"=", b"")
    return eid.decode("utf-8")


def decode(e, sub_key):
    if isinstance(e, basestring):
        e = bytes(e.encode("ascii"))
    
    try:
        forced_version = None
        if e.startswith(b"$"):
            forced_version = 1
            e = e[1:]
    except AttributeError:
        raise EncryptedIDDecodeError()

    try:
        padding = (3 - len(e) % 3) * b"="
        e = base64.urlsafe_b64decode(e + padding)
    except (TypeError, AttributeError, binascii.Error):
        raise EncryptedIDDecodeError()

    for key in getattr(settings, "SECRET_KEYS", [settings.SECRET_KEY]):
        iv = hashlib.sha256((key + sub_key).encode('ascii')).digest()[:16]
        cypher = AES.new(key[:32].encode('utf-8'), AES.MODE_CBC, iv)
        try:
            msg = cypher.decrypt(e)
        except ValueError:
            raise EncryptedIDDecodeError()

        try:
            crc, the_id, version = struct.unpack(b"<IQI", msg)
        except struct.error:
            raise EncryptedIDDecodeError()

        if forced_version is not None:
            version = forced_version

        try:
            if version == 0:
                expected_crc = binascii.crc32(bytes(the_id)) & 0xffffffff
            else:
                id_str = str(the_id).encode('utf-8')
                expected_crc = binascii.crc32(id_str) & 0xffffffff
        except (MemoryError, OverflowError):
            raise EncryptedIDDecodeError()

        if crc != expected_crc:
            continue

        return the_id
    raise EncryptedIDDecodeError("Failed to decrypt, CRC never matched.")


def get_model_sub_key(m):
    try:
        return m._meta.ek_key
    except AttributeError:
        return m._meta.db_table


def get_object_or_404(m, ekey, *arg, **kw):
    try:
        pk = decode(ekey, get_model_sub_key(m))
    except EncryptedIDDecodeError:
        raise Http404

    return go4(m, id=pk, *arg, **kw)


def ekey(instance):
    assert isinstance(instance, Model)
    return encode(instance.id, get_model_sub_key(instance))
