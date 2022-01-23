import pytest
from django.http import Http404
from django.test import TestCase

from encrypted_id import ekey, get_object_or_404
from tests.testapp.models import Foo

pytestmark = pytest.mark.django_db


class TestEkey(TestCase):
    def test_ekey(self):
        foo = Foo.objects.create(text="asd")
        assert ekey(foo) == foo.ekey

    def test_ekey_query(self):
        foo = Foo.objects.create(text="asd")
        assert foo == Foo.objects.get(ekey=foo.ekey)

    def test_ekey_get_object_or_404(self):
        foo = Foo.objects.create(text="asd")
        assert foo == get_object_or_404(model=Foo, ekey=foo.ekey)

    def test_get_object_or_404_raises_404(self):
        with pytest.raises(Http404):
            get_object_or_404(model=Foo, ekey=None)

    def test_query_ekey_none_raises_does_not_exist(self):
        with pytest.raises(Foo.DoesNotExist):
            Foo.objects.get(ekey=None)
