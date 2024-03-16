"""Handlers for bibliography."""

from wagtail.admin.rich_text.converters.html_to_contentstate import LinkElementHandler
from wagtail.rich_text import LinkHandler

from django.conf import settings


class BibliographyLinkHandler(LinkHandler):
    identifier = 'biblio_entry'

    @classmethod
    def expand_db_attributes(cls, attrs):
        attributes = attrs['id']
        return f'<a href="{settings.PUBLIC_URL}/project/bibliography/#{attributes}">'


class BibliographyElementHandler(LinkElementHandler):
    def get_attribute_data(self, attrs):
        # TODO: generalize url
        return {
            'id': attrs['id'],
            'url': f'{settings.PUBLIC_URL}/project/bibliography/#{attrs["id"]}/',
            'parentId': 'biblio_entry',
        }
