"""URLs for footnotes extension."""

from django.urls import path

from .views import footnote

urlpatterns = [
    path('footnote/', footnote, name='footnote_chooser'),
]
