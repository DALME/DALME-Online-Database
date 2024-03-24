"""Handlers for saved search."""

from wagtail.admin.rich_text.converters.html_to_contentstate import LinkElementHandler
from wagtail.rich_text import LinkHandler

from django.utils.html import escape

from ida.models import SavedSearch


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
            return {
                'id': _id,
                'url': f'/collections/search/{_id}/',
                'parentId': 'saved_search',
            }

        return {
            'id': str(saved_search.id),
            'url': f'/collections/search/{saved_search.id!s}/',
            'parentId': 'saved_search',
        }
