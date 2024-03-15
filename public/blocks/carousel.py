"""Image carousel block."""

from wagtail import blocks


class CarouselBlock(blocks.ListBlock):
    class Meta:
        icon = 'cogs'
        template = 'public/blocks/_carousel.html'
