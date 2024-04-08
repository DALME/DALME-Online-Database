"""Blocks for footnotes extension."""

from wagtail import blocks


class FootnotesPlaceMarker(blocks.StructBlock):
    class Meta:
        icon = 'list-ol'
        template = 'footnote_placemarker.html'
