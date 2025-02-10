"""URLs for footnotes extension."""

from django.urls import path

from .views import FootnoteChooser

urlpatterns = [
    path('footnote/', FootnoteChooser.as_view(), name='footnote_chooser'),
    path('footnote/<uuid:pk>/', FootnoteChooser.as_view()),
]
