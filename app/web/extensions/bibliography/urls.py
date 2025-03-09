"""URLs for bibliography extension."""

from django.urls import path

from .views import ReferenceChooser

urlpatterns = [
    path('reference/', ReferenceChooser.as_view(), name='reference_chooser'),
]
