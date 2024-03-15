"""Main image block."""

from wagtail.images.blocks import ImageChooserBlock


class MainImageBlock(ImageChooserBlock):
    class Meta:
        icon = 'image'
        template = 'public/blocks/_main_image.html'
