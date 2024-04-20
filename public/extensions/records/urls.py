"""URLs for records extension."""

from wagtail.api.v2.router import WagtailAPIRouter

from django.urls import path

from .api import FilterChoices, RecordsAPIViewSet, ThumbnailsAPI
from .views import SavedSearchChooser

api_router = WagtailAPIRouter('wagtailapi')

api_router.register_endpoint('records', RecordsAPIViewSet)
api_router.register_endpoint('thumbnails', ThumbnailsAPI)
api_router.register_endpoint('choices', FilterChoices)


urlpatterns = [
    path('savedsearch/', SavedSearchChooser.as_view(), name='saved_search_chooser'),
]
