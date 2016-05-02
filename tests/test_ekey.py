# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from encrypted_id import ekey, get_object_or_404
from tapp.models import Foo


def test_ekey(db):
    assert db is db

    foo = Foo.objects.create(text="asd")
    assert ekey(foo) == foo.ekey
    assert foo == get_object_or_404(Foo, foo.ekey)
