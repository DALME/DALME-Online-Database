"""Subsection blocks."""

from wagtail import blocks


class SubsectionBlock(blocks.StructBlock):
    subsection = blocks.CharBlock()
    collapsed = blocks.BooleanBlock(required=False, default=True)
    minor_heading = blocks.BooleanBlock(required=False, default=False)

    class Meta:
        icon = 'collapse-down'
        template = 'public/blocks/subsection.html'


class SubsectionEndMarkerBlock(blocks.StructBlock):
    """Block for marking the end of a subsection."""

    class Meta:
        icon = 'collapse-up'
        template = 'public/blocks/subsection_end.html'
