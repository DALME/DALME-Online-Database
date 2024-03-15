"""Block for marking where footnotes should be inserted."""

from wagtail import blocks


class FootnotesPlaceMarker(blocks.StructBlock):
    class Meta:
        icon = 'list-ol'
        template = 'public/blocks/_footnote_placemarker.html'
