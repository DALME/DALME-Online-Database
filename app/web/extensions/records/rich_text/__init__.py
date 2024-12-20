"""Interface for the records rich_text module."""

from wagtail.rich_text import LinkHandler


class SavedSearchLinkHandler(LinkHandler):
    identifier = 'saved_search'

    @classmethod
    def expand_db_attributes(cls, attrs):
        search_id = attrs['id']
        return f'<a href="/collections/search/{search_id}/">'
