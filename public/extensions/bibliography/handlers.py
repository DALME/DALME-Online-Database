"""Handlers for references."""

from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler
from wagtail.rich_text import LinkHandler

from django.conf import settings

UUIDv4 = r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$'


class ReferenceLinkHandler(LinkHandler):
    identifier = 'reference'

    @classmethod
    def expand_db_attributes(cls, attrs):
        ref_id = attrs['id']
        # TODO: generalize url: call bibliography page and get url from it
        return f'<a href="{settings.PUBLIC_URL}/project/bibliography/#{ref_id}">'


class ReferenceElementHandler(InlineEntityElementHandler):
    """Convert the a tag into a REFERENCE entity, with the right data."""

    mutability = 'IMMUTABLE'

    # TODO: generalize url: call bibliography page and get url from it
    def get_attribute_data(self, attrs):
        return {
            'id': attrs['id'],
            'url': f'{settings.PUBLIC_URL}/project/bibliography/#{attrs["id"]}/',
        }


def reference_entity_decorator(props):
    """Convert the REFERENCE entities into an a tag."""
    return DOM.create_element(
        'a',
        {
            'href': f'{settings.PUBLIC_URL}/project/bibliography/#{props["id"]}',
        },
        props['children'],
    )
