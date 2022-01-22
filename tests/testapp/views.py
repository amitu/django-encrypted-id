from django.views.generic import DetailView

from tests.testapp.models import Foo


class FooView(DetailView):
    model = Foo
    slug_field = 'ekey'
    template_name = 'admin/actions.html'
