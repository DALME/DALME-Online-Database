"""Main image block."""

from wagtail.images.blocks import ImageChooserBlock


class MainImageBlock(ImageChooserBlock):
    class Meta:
        icon = 'panorama'
        template = 'main_image_block.html'
