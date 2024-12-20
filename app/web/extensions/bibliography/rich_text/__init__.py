"""Interface for the bibliography/reference rich_text module."""

from wagtail.rich_text import LinkHandler

from django.conf import settings


class ReferenceLinkHandler(LinkHandler):
    """Translate the content of rich text tags into front-end HTML."""

    identifier = 'reference'

    @classmethod
    def expand_db_attributes(cls, attrs):
        ref_id = attrs['data-id']
        # TODO: generalize url: call bibliography page and get url from it
        return f'<a href="{settings.PUBLIC_URL}/project/bibliography/#{ref_id}">'
