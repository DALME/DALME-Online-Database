"""Interface for the public.handlers module."""

import re

from draftjs_exporter.dom import DOM

from .bibliography import BibliographyElementHandler, BibliographyLinkHandler
from .footnote import FootnoteElementHandler, footnote_decorator
from .saved_search import SavedSearchElementHandler, SavedSearchLinkHandler

UUIDv4 = r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$'


def link_entity_decorator(props):
    id_ = props.get('id')
    link_props = {}

    if id_ is not None and id_ != '':
        if str(id_).isdigit():
            link_props['linktype'] = 'page'
        elif re.fullmatch(UUIDv4, id_):
            link_props['linktype'] = 'saved_search'
        else:
            link_props['linktype'] = 'biblio_entry'

        link_props['id'] = id_

    else:
        link_props['href'] = props.get('url')

    return DOM.create_element('a', link_props, props['children'])


__all__ = [
    'BibliographyElementHandler',
    'BibliographyLinkHandler',
    'FootnoteElementHandler',
    'footnote_decorator',
    'link_entity_decorator',
    'SavedSearchElementHandler',
    'SavedSearchLinkHandler',
]
