"""Interface for the public.extensions.savedsearches module."""

from .handlers import SavedSearchElementHandler, SavedSearchLinkHandler
from .hooks import add_savedsearch_js_to_editor
from .urls import urlpatterns

# link from_database_format rule
savedsearch_from_link_rule = ('a[linktype="saved_search"]', SavedSearchElementHandler('LINK'))


__all__ = [
    'add_savedsearch_js_to_editor',
    'savedsearch_from_link_rule',
    'SavedSearchLinkHandler',
    'urlpatterns',
]
