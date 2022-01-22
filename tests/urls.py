from django.urls import path
from tests.testapp.views import FooView

urlpatterns = [
    path('foo/<str:slug>/', FooView.as_view(), name='foo'),
]
