"""Interface for the api module of the images extension."""

from wagtail.images.api.v2.views import ImagesAPIViewSet


class WebImageAPIViewSet(ImagesAPIViewSet):
    body_fields = [*ImagesAPIViewSet.body_fields, 'caption']
