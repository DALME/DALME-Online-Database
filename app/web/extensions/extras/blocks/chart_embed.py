"""Block for embedding charts."""

from wagtail import blocks

from web.extensions.extras.widgets import CustomSelect


class ChartEmbedBlock(blocks.StructBlock):
    html = blocks.RawHTMLBlock(
        help_text='Embed code for the chart.',
    )
    alignment = blocks.ChoiceBlock(
        choices=[
            ('left', 'Left-aligned'),
            ('right', 'Right-aligned'),
            ('full', 'Full-width'),
        ],
        help_text='How should the chart be aligned on the page?',
        widget=CustomSelect,
    )

    class Meta:
        icon = 'chart-area'
        template = 'extras/chart_embed_block.html'
