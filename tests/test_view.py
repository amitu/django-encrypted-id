from django.test import Client
from django.urls import reverse

from tests.testapp.models import Foo


def test_view(db):
    assert db is db

    client = Client()

    foo = Foo.objects.create(text="hello")
    url = reverse("foo", kwargs={'slug': foo.ekey})
    response = client.get(url)
    response_object = response.context["object"]
    assert response_object == foo
