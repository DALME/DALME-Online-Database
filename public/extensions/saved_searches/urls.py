"""URLs for saved searches extension."""

from django.urls import path

from .views import saved_search

urlpatterns = [
    path('choose-saved-search/', saved_search, name='wagtailadmin_choose_saved_search'),
]
