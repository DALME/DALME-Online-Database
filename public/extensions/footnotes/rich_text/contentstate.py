"""Footnote Draftail/contentstate conversion."""

from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler

from public.extensions.footnotes.models import Footnote


class FootnoteElementHandler(InlineEntityElementHandler):
    mutability = 'IMMUTABLE'

    def get_attribute_data(self, attrs):
        instance = Footnote.objects.get(id=attrs['data-footnote'])
        return {
            'id': attrs['data-footnote'],
            'page': instance.page.id,
            'text': instance.text,
            'linktype': 'footnote',
        }


def footnote_decorator(props):
    return DOM.create_element(
        'a',
        {
            'data-footnote': props['id'],
            'linktype': 'footnote',
        },
        props['children'],
    )
