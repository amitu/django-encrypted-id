import pytest
from django.http import Http404

from encrypted_id import ekey, get_object_or_404
from tests.testapp.models import Foo

pytestmark = pytest.mark.django_db


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
