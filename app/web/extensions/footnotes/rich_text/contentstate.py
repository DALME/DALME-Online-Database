"""Footnote Draftail/contentstate conversion."""

from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler

from web.extensions.footnotes.models import Footnote


class FootnoteElementHandler(InlineEntityElementHandler):
    """Convert database HTML to ContentState as a REFERENCE entity, with the right data."""

    mutability = 'IMMUTABLE'

    def get_attribute_data(self, attrs):
        instance = Footnote.objects.get(id=attrs['data-footnote'])
        return {
            'id': attrs['data-footnote'],
            'text': instance.text,
            'linktype': 'footnote',
        }


def footnote_decorator(props):
    """Convert ContentState REFERENCE entities into database HTML."""
    return DOM.create_element(
        'a',
        {
            'data-footnote': props.get('id'),
            'linktype': 'footnote',
        },
        props['children'],
    )
