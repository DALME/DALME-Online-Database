"""Handlers for bibliography."""

from wagtail.admin.rich_text.converters.html_to_contentstate import LinkElementHandler
from wagtail.rich_text import LinkHandler


class BibliographyLinkHandler(LinkHandler):
    identifier = 'biblio_entry'

    @classmethod
    def expand_db_attributes(cls, attrs):
        # TODO: generalize url
        return '<a href="https://dalme.org/project/bibliography/#' + attrs['id'] + '">'


class BibliographyElementHandler(LinkElementHandler):
    def get_attribute_data(self, attrs):
        # TODO: generalize url
        return {
            'id': attrs['id'],
            'url': f'https://dalme.org/project/bibliography/#{attrs["id"]}/',
            'parentId': 'biblio_entry',
        }
