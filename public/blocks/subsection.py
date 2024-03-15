"""Subsection block."""

from wagtail import blocks


class SubsectionBlock(blocks.StructBlock):
    subsection = blocks.CharBlock()
    collapsed = blocks.BooleanBlock(required=False, default=True)
    minor_heading = blocks.BooleanBlock(required=False, default=False)

    class Meta:
        icon = 'collapse-down'
        template = 'public/blocks/_subsection.html'
