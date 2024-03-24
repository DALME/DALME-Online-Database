"""External resource block."""

from wagtail import blocks


class ExternalResourceBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    info = blocks.CharBlock()
    url = blocks.URLBlock()
    date = blocks.DateBlock()

    class Meta:
        icon = 'link'
        template = 'public/blocks/external_resource.html'
