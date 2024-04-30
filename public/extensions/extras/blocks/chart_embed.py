"""Block for embedding charts."""

from wagtail import blocks


class ChartEmbedBlock(blocks.StructBlock):
    html = blocks.RawHTMLBlock()
    alignment = blocks.ChoiceBlock(
        choices=[
            ('left', 'Left-aligned'),
            ('right', 'Right-aligned'),
            ('full', 'Full-width'),
        ],
    )

    class Meta:
        icon = 'chart-area'
        template = 'chart_embed_block.html'
