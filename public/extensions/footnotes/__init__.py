"""Interface for the public.extensions.footnotes module."""

from .blocks import FootnotesPlaceMarker
from .hooks import add_footnotes_js_to_editor, enable_footnotes
from .urls import urlpatterns

__all__ = [
    'add_footnotes_js_to_editor',
    'enable_footnotes',
    'FootnotesPlaceMarker',
    'urlpatterns',
]
