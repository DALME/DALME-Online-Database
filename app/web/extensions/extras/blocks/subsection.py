"""Subsection block."""

from wagtail import blocks


class NestedSubsectionBlock(blocks.StructBlock):
    subsection = blocks.CharBlock(
        label='Title',
        help_text='Subsection title.',
    )
    collapsed = blocks.BooleanBlock(required=False, default=False, help_text='Render closed.')
    minor_heading = blocks.BooleanBlock(label='Minor', required=False, default=False, help_text='Render indented.')

    def __init__(self, **kwargs):
        from web.extensions.block_registry import STREAMFIELD_INTERFACE, BlockRegistry

        interface = [b for b in STREAMFIELD_INTERFACE if b != 'subsection']
        definition = BlockRegistry.block_def(interface)
        block = blocks.StreamBlock(definition)
        self.body = block

        super().__init__(**kwargs)

    class Meta:
        icon = 'diagram-successor'
        label = 'Subsection'
        template = 'extras/subsection_block.html'
        form_classname = 'struct-block subsection-block'


class SubsectionBlock(NestedSubsectionBlock):
    def __init__(self, **kwargs):
        from web.extensions.block_registry import STREAMFIELD_INTERFACE, BlockRegistry

        interface = [b for b in STREAMFIELD_INTERFACE if b != 'subsection']
        definition = BlockRegistry.block_def(interface)
        definition = [*definition, ('nested_subsection', NestedSubsectionBlock())]
        block = blocks.StreamBlock(definition)
        self.body = block

        super().__init__(**kwargs)

    class Meta:
        icon = 'diagram-next'
        label = 'Subsection'
        template = 'extras/subsection_block.html'
        form_classname = 'struct-block subsection-block'
