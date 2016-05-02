# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from tapp.models import Foo, Foo2
from django.http import Http404
import pytest


def test_model(db):
    assert db is db

    foo = Foo.objects.create(text="hello")
    assert foo.ekey
    assert foo == Foo.objects.get_by_ekey(foo.ekey)
    assert foo == Foo.objects.get_by_ekey_or_404(foo.ekey)

    foo = Foo2.objects.create(text="hello")
    assert foo.ekey
    assert foo == Foo2.objects.get_by_ekey(foo.ekey)
    assert foo == Foo2.objects.get_by_ekey_or_404(foo.ekey)

    with pytest.raises(Http404):
        Foo.objects.get_by_ekey_or_404("123123")
