"""Interface for the footnotes rich_text module."""

from wagtail.rich_text import LinkHandler


class FootnoteLinkHandler(LinkHandler):
    identifier = 'footnote'

    @classmethod
    def expand_db_attributes(cls, attrs):
        fn_id = attrs['data-footnote']
        return f'<a href="#fn_{fn_id}" class="footnote_callout" id="{fn_id}">'
