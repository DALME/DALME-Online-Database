"""Subsection blocks."""

from wagtail import blocks


class SubsectionBlock(blocks.StructBlock):
    subsection = blocks.CharBlock(
        label='Title',
        help_text='Subsection title.',
    )
    collapsed = blocks.BooleanBlock(required=False, default=False, help_text='Render closed.')
    minor_heading = blocks.BooleanBlock(label='Minor', required=False, default=False, help_text='Render indented.')

    class Meta:
        icon = 'diagram-successor'
        template = 'public/blocks/subsection.html'
        form_classname = 'struct-block subsection-block'


class SubsectionEndMarkerBlock(blocks.StructBlock):
    """Block for marking the end of a subsection."""

    class Meta:
        icon = 'diagram-next'
        template = 'public/blocks/subsection_end.html'
        help_text = 'This block is used to indicate the end of a subsection in cases where it is followed by something other than another subsection or the end of the page.'
