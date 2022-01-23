import pytest
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from tests.testapp.models import Bar, Foo, Foo2

pytestmark = pytest.mark.django_db


class TestModel(TestCase):
    def test_model(self):
        foo = Foo.objects.create(text="hello")
        assert foo.ekey
        assert foo == Foo.objects.get_by_ekey(foo.ekey)
        assert foo == Foo.objects.get_by_ekey_or_404(foo.ekey)
        assert foo == Foo.objects.get(ekey=foo.ekey)
        assert foo == Foo.objects.filter(ekey=foo.ekey).get()

        foo = Foo2.objects.create(text="hello2")
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

    def test_sub_key(self):
        foo = Foo.objects.create(text="hello")

        try:
            foo2 = Foo2.objects.get(pk=foo.pk)
        except ObjectDoesNotExist:
            foo2 = Foo2.objects.create(pk=foo.pk, text="hello")

        try:
            bar = Bar.objects.get(pk=foo.pk)
        except ObjectDoesNotExist:
            bar = Bar.objects.create(pk=foo.pk, text="hello")

        assert foo.pk == foo2.pk == bar.pk
        assert foo.ekey == foo2.ekey
        assert foo.ekey != bar.ekey
