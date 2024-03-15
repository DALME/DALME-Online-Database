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
        icon = 'image'
        template = 'public/blocks/_chart_embed.html'
