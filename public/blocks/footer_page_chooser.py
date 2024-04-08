"""Chooser block to select pages to include in footer as links."""

from wagtail import blocks


class FooterPageChooserBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    page = blocks.PageChooserBlock()

    class Meta:
        icon = 'link'
        template = 'public/blocks/footer_page.html'
