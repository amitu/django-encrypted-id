# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest
from django.http import Http404

from encrypted_id import ekey, get_object_or_404
from tapp.models import Foo, Bar


def test_ekey(db):
    assert db is db

    foo = Foo.objects.create(text="asd")
    assert ekey(foo) == foo.ekey
    assert foo == get_object_or_404(Foo, foo.ekey)


def test_allow_none_ekey(db):
    assert db is db

    with pytest.raises(Http404):
        get_object_or_404(Foo, None)

    with pytest.raises(Foo.DoesNotExist):
        Foo.objects.get(ekey=None)

    with pytest.raises(Bar.DoesNotExist):
        Bar.objects.get(foo__ekey=None)
