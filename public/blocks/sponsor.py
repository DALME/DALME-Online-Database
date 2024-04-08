"""Block for showing sponsors in home page."""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class SponsorBlock(blocks.StructBlock):
    logo = ImageChooserBlock()
    url = blocks.URLBlock()

    class Meta:
        icon = 'hand-holding-heart'
        template = 'public/blocks/sponsor.html'
