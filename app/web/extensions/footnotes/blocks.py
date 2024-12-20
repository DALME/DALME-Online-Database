"""Blocks for footnotes extension."""

from wagtail import blocks


class FootnotesPlaceMarker(blocks.StructBlock):
    class Meta:
        icon = 'list-ol'
        template = 'footnote_container.html'
        help_text = 'This block is used to indicate where the footnotes in the page should be placed.'
