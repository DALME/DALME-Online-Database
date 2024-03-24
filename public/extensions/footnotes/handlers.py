"""Handlers for footnote."""

from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler


class FootnoteElementHandler(InlineEntityElementHandler):
    mutability = 'IMMUTABLE'

    def get_attribute_data(self, attrs):
        # Take values from the HTML data attributes.
        return {
            'note_id': attrs['data-note_id'],
            'text': attrs['data-footnote'],
        }


def footnote_decorator(props):
    return DOM.create_element(
        'span',
        {
            'data-note_id': props['note_id'],
            'data-footnote': props['text'],
        },
        props['children'],
    )
