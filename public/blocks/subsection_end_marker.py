"""Block for marking the end of a subsection."""

from wagtail import blocks


class SubsectionEndMarkerBlock(blocks.StructBlock):
    class Meta:
        icon = 'collapse-up'
        template = 'public/blocks/_subsection_end.html'
