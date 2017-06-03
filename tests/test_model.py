# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from tapp.models import Foo, Foo2
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import Http404
import pytest


def test_model(db):
    assert db is db

    foo = Foo.objects.create(text="hello")
    assert foo.ekey
    assert foo == Foo.objects.get_by_ekey(foo.ekey)
    assert foo == Foo.objects.get_by_ekey_or_404(foo.ekey)
    assert foo == Foo.objects.get(ekey=foo.ekey)
    assert foo == Foo.objects.filter(ekey=foo.ekey).get()

    foo = Foo2.objects.create(text="hello")
    assert foo.ekey
    assert foo == Foo2.objects.get_by_ekey(foo.ekey)
    assert foo == Foo2.objects.get_by_ekey_or_404(foo.ekey)
    assert foo == Foo2.objects.get(ekey=foo.ekey)
    assert foo == Foo2.objects.filter(ekey=foo.ekey).get()

    with pytest.raises(Http404):
        Foo.objects.get_by_ekey_or_404("123123")

    with pytest.raises(Http404):
        get_list_or_404(Foo, ekey="123123")

    with pytest.raises(Http404):
        get_object_or_404(Foo, ekey="123123")
