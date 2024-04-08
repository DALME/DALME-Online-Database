"""Footnotes API endpoint."""

from wagtail.api.v2.views import BaseAPIViewSet

from django.urls import path

from .models import Footnote
from .serializers import FootnoteSerializer


class FootnotesAPIViewSet(BaseAPIViewSet):
    base_serializer_class = FootnoteSerializer
    name = 'footnotes'
    model = Footnote

    @classmethod
    def get_urlpatterns(cls):
        return [
            path('', cls.as_view({'get': 'listing_view'}), name='listing'),
            path('<uuid:pk>/', cls.as_view({'get': 'detail_view'}), name='detail'),
        ]

    def get_serializer_class(self):
        return self.base_serializer_class
