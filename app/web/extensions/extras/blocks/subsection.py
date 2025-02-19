"""Subsection block."""

from wagtail import blocks

from .defaults import BASE_BLOCKS


class NestedSubsectionBlock(blocks.StructBlock):
    subsection = blocks.CharBlock(
        label='Title',
        help_text='Subsection title.',
    )
    collapsed = blocks.BooleanBlock(required=False, default=False, help_text='Render closed.')
    minor_heading = blocks.BooleanBlock(label='Minor', required=False, default=False, help_text='Render indented.')
    body = blocks.StreamBlock(BASE_BLOCKS)

    class Meta:
        icon = 'diagram-successor'
        label = 'Subsection'
        template = 'extras/nested_extras/subsection_block.html'
        form_classname = 'struct-block subsection-block'


EXTENDED_BLOCKS = [
    *BASE_BLOCKS,
    ('nested_subsection', NestedSubsectionBlock()),
]


class SubsectionBlock(NestedSubsectionBlock):
    body = blocks.StreamBlock(EXTENDED_BLOCKS)

    class Meta:
        icon = 'diagram-next'
        label = 'Subsection'
        template = 'extras/subsection_block.html'
        form_classname = 'struct-block subsection-block'
