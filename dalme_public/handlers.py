from wagtail.rich_text import LinkHandler
from wagtail.admin.rich_text.converters.html_to_contentstate import LinkElementHandler, InlineEntityElementHandler
from django.utils.html import escape
from dalme_app.models import SavedSearch
from draftjs_exporter.dom import DOM
import re

UUIDv4 = r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$'


class SavedSearchLinkHandler(LinkHandler):
    identifier = 'saved_search'

    @staticmethod
    def get_model():
        return SavedSearch

    @classmethod
    def get_instance(cls, attrs):
        model = cls.get_model()
        return model.objects.get(id=attrs['id'])

    @classmethod
    def expand_db_attributes(cls, attrs):
        search = cls.get_instance(attrs)
        href = f'/collections/search/{search.id}/'
        return f'<a href="{escape(href)}">'


class SavedSearchElementHandler(LinkElementHandler):
    def get_attribute_data(self, attrs):
        try:
            saved_search = SavedSearch.objects.get(id=attrs['id'])
        except SavedSearch.DoesNotExist:
            _id = int(attrs['id'])
            return {'id': _id, 'url': f'/collections/search/{_id}/', 'parentId': 'saved_search'}

        return {
            'id': str(saved_search.id),
            'url': f'/collections/search/{str(saved_search.id)}/',
            'parentId': 'saved_search',
        }


class BibliographyLinkHandler(LinkHandler):
    identifier = 'biblio_entry'

    @classmethod
    def expand_db_attributes(cls, attrs):
        return '<a href="https://dalme.org/project/bibliography/#' + attrs['id'] + '">'


class BibliographyElementHandler(LinkElementHandler):
    def get_attribute_data(self, attrs):
        return {
            'id': attrs['id'],
            'url': f'https://dalme.org/project/bibliography/#{attrs["id"]}/',
            'parentId': 'biblio_entry',
        }


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
