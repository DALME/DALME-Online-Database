from wagtail.core.rich_text import LinkHandler
from wagtail.admin.rich_text.converters.html_to_contentstate import LinkElementHandler
from django.utils.html import escape
from dalme_app.models import SavedSearch
from draftjs_exporter.dom import DOM


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
        return '<a href="%s">' % escape(href)


class SavedSearchElementHandler(LinkElementHandler):
    def get_attribute_data(self, attrs):
        try:
            saved_search = SavedSearch.objects.get(id=attrs['id'])
        except SavedSearch.DoesNotExist:
            return {
                'id': int(attrs['id']),
                'url': None,
                'parentId': None
            }

        return {
            'id': str(saved_search.id),
            'url': f'/collections/search/{str(saved_search.id)}/',
            'parentId': None,
        }


def link_entity_search(props):
    id_ = props.get('id')
    link_props = {}

    if id_ is not None:
        link_props['linktype'] = 'page' if type(id_) is int else 'saved_search'
        link_props['id'] = id_
    else:
        link_props['href'] = props.get('url')

    return DOM.create_element('a', link_props, props['children'])
