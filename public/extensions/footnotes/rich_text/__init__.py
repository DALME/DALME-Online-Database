"""Interface for the footnotes rich_text module."""

from wagtail.rich_text import LinkHandler

from public.extensions.footnotes.models import Footnote


class FootnoteLinkHandler(LinkHandler):
    identifier = 'footnote'

    @classmethod
    def expand_db_attributes(cls, attrs):
        try:
            instance = Footnote.objects.get(pk=attrs['data-footnote'])
        except Footnote.DoesNotExist:
            return ''
        else:
            return f'<a href="#fn_{instance.id}" class="footnote_callout" id="{instance.id}" data-index="{instance.sort_order}">'
