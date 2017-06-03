# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import Client

from tapp.models import Foo


def test_view(db):
    assert db is db

    client = Client()

    foo = Foo.objects.create(text="hello")
    url = reverse("foo", args=(foo.ekey,))
    response = client.get(url)
    response_object = response.context["object"]
    assert response_object == foo
