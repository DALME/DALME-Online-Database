"""Interface for the public.extensions.savedsearches module."""

from .handlers import SavedSearchElementHandler, SavedSearchLinkHandler
from .urls import urlpatterns
from .wagtail_hooks import add_savedsearch_js_to_editor

# link from_database_format rule
savedsearch_from_link_rule = ('a[linktype="saved_search"]', SavedSearchElementHandler('LINK'))


__all__ = [
    'add_savedsearch_js_to_editor',
    'savedsearch_from_link_rule',
    'SavedSearchLinkHandler',
    'urlpatterns',
]
