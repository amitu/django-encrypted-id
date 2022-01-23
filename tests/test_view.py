import pytest
from django.test import Client
from django.urls import reverse

from tests.testapp.models import Foo
from django.test import TestCase

pytestmark = pytest.mark.django_db


class TestView(TestCase):
    def test_view(self):
        client = Client()

        foo = Foo.objects.create(text="hello")
        url = reverse("foo", kwargs={'slug': foo.ekey})
        response = client.get(url)
        response_object = response.context["object"]
        assert response_object == foo
