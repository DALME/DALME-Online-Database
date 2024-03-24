"""Interface for the public.extensions.bibliography module."""

from .blocks import BibliographyChooserBlock
from .handlers import ReferenceLinkHandler
from .hooks import add_reference_js_to_editor, register_reference_feature

# from .urls import urlpatterns
from .views import BiblioChooserViewSet, BiblioViewSet, ReferenceChooserViewSet

# link from_database_format rule
# biblio_from_link_rule = ('a[linktype="reference"]', ReferenceElementHandler('LINK'))

__all__ = [
    'add_reference_js_to_editor',
    'biblio_from_link_rule',
    'BiblioChooserViewSet',
    'BiblioViewSet',
    'BibliographyChooserBlock',
    'ReferenceLinkHandler',
    'register_reference_feature',
    'ReferenceChooserViewSet',
    'urlpatterns',
]
