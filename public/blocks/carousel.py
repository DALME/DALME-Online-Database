"""Image carousel block."""

from wagtail import blocks


class CarouselBlock(blocks.ListBlock):
    class Meta:
        icon = 'photo-film'
        template = 'public/blocks/carousel.html'
