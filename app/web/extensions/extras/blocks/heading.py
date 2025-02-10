"""Heading block."""

from wagtail import blocks

from web.extensions.extras.widgets import CustomSelect

from .uncommented_charblock import UncommentedCharBlock


class HeadingBlock(blocks.StructBlock):
    heading = UncommentedCharBlock(required=True)
    level = blocks.ChoiceBlock(
        choices=[
            ('h1', 'H1'),
            ('h2', 'H2'),
            ('h3', 'H3'),
            ('h4', 'H4'),
        ],
        default='h1',
        required=False,
        widget=CustomSelect,
    )

    class Meta:
        icon = 'heading'
        label = 'Heading'
        template = 'heading_block.html'
        form_classname = 'struct-block heading-block'
        form_template = 'heading_form.html'
