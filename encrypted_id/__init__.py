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
import struct

from django.conf import settings
from django.db.models import Model
from django.http import Http404
from django.shortcuts import get_object_or_404 as go4


__version__ = "0.1.2"
__license__ = "BSD"
__author__ = "Amit Upadhyay"
__email__ = "upadhyay@gmail.com"
__url__ = "http://amitu.com/encrypted-id/"
__source__ = "https://github.com/amitu/django-encrypted-id"
__docformat__ = "html"


def encode(the_id):
    assert 0 <= the_id < 2 ** 64

    crc = binascii.crc32(bytes(the_id)) & 0xffffffff

    message = struct.pack(b"<IQxxxx", crc, the_id)
    assert len(message) == 16

    cypher = AES.new(
        settings.SECRET_KEY[:24], AES.MODE_CBC,
        settings.SECRET_KEY[-16:]
    )

    return base64.urlsafe_b64encode(cypher.encrypt(message)).replace(b"=", b".")


def decode(e):
    if isinstance(e, str):
        e = bytes(e.encode("ascii"))

    try:
        e = base64.urlsafe_b64decode(e.replace(b".", b"="))
    except (TypeError, AttributeError):
        raise ValueError("Failed to decrypt, invalid input.")

    cypher = AES.new(
        encrypted_id_setting['SECRET_KEYS'][:24], AES.MODE_CBC,
        encrypted_id_setting['SECRET_KEYS'][-16:]
    )

    message = cypher.decrypt(e)
    crc, the_id = struct.unpack("<IQxxxx", message)

    if crc == binascii.crc32(bytes(the_id)) & 0xffffffff:
        return the_id

    raise ValueError("Failed to decrypt, CRC never matched.")


def get_object_or_404(m, ekey, *arg, **kw):
    try:
        pk = decode(ekey)
    except ValueError:
        raise Http404

    return go4(m, id=pk, *arg, **kw)


def ekey(instance):
    assert isinstance(instance, Model)
    return encode(instance.id)
