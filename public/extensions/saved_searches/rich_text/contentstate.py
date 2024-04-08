"""Saved search Draftail/contentstate conversion."""

from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler


class SavedSearchElementHandler(InlineEntityElementHandler):
    mutability = 'IMMUTABLE'

    def get_attribute_data(self, attrs):
        return {
            'id': attrs['id'],
            'name': attrs['data-saved-search'],
            'linktype': 'saved_search',
        }


def saved_search_decorator(props):
    return DOM.create_element(
        'a',
        {
            'id': props['id'],
            'data-saved-search': props['name'],
            'linktype': 'saved_search',
        },
        props['children'],
    )
