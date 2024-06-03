"""URLs for records extension."""

from django.urls import path

from .views import SavedSearchChooser

urlpatterns = [
    path('savedsearch/', SavedSearchChooser.as_view(), name='saved_search_chooser'),
]
