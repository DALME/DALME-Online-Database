"""Interface for the public.extensions module."""

import re
import urllib

from draftjs_exporter.dom import DOM

from django.http import HttpResponseRedirect
from django.urls import path, reverse

# from .bibliography import ReferenceLinkHandler, biblio_from_link_rule
# from .bibliography import urlpatterns as biblio_urls
from .footnotes import urlpatterns as footnote_urls
from .saved_searches import SavedSearchLinkHandler, savedsearch_from_link_rule
from .saved_searches import urlpatterns as search_urls

UUIDv4 = r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$'

LINK_FROM_RULES_REGISTER = [
    # biblio_from_link_rule,
    savedsearch_from_link_rule,
]

LINK_HANDLERS_REGISTER = [
    # ReferenceLinkHandler,
    SavedSearchLinkHandler,
]


def link_entity_decorator(props):
    id_ = props.get('id')
    link_props = {}

    if id_ is not None and id_ != '':
        if str(id_).isdigit():
            link_props['linktype'] = 'page'
        elif re.fullmatch(UUIDv4, id_):
            link_props['linktype'] = 'saved_search'
        # else:
        #     link_props['linktype'] = 'reference'

        link_props['id'] = id_

    else:
        link_props['href'] = props.get('url')

    return DOM.create_element('a', link_props, props['children'])


def reroute_chooser(request, route=None):
    """View for rerouting chooser modals."""
    params = urllib.parse.urlencode(request.GET)

    if route:
        if str(route).isdigit():
            rev = reverse('wagtailadmin_choose_page_child', args=[route])
        elif route == 'saved_search':
            rev = reverse('wagtailadmin_choose_saved_search')
        # elif route == 'reference':
        #     rev = reverse('wagtailadmin_choose_reference')
    else:
        rev = reverse('wagtailadmin_choose_page')

    if params:
        rev = f'{rev}?{params}'

    return HttpResponseRedirect(rev)


urlpatterns = [
    # *biblio_urls,
    *search_urls,
    *footnote_urls,
    path('choose-reroute/', reroute_chooser, name='wagtailadmin_chooser_page_reroute'),
    path('choose-reroute/<slug:route>/', reroute_chooser, name='wagtailadmin_chooser_page_reroute_child'),
]

__all__ = [
    'LINK_FROM_RULES_REGISTER',
    'link_entity_decorator',
    'LINK_HANDLERS_REGISTER',
    'urlpatterns',
]
