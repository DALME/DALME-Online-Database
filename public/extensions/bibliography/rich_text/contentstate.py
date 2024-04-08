"""Reference Draftail/contentstate conversion."""

from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler


class ReferenceElementHandler(InlineEntityElementHandler):
    """Convert database HTML to ContentState as a REFERENCE entity, with the right data."""

    mutability = 'IMMUTABLE'

    # TODO: generalize url: call bibliography page and get url from it
    def get_attribute_data(self, attrs):
        return {
            'biblio': attrs['data-biblio'],
            'id': attrs['data-id'],
            'reference': attrs['data-reference'],
            'linktype': 'reference',
        }


def reference_decorator(props):
    """Convert ContentState REFERENCE entities into database HTML."""
    return DOM.create_element(
        'a',
        {
            'data-biblio': props['biblio'],
            'data-id': props['id'],
            'data-reference': props['reference'],
            'linktype': 'reference',
        },
        props['children'],
    )
