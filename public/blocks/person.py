"""Person block."""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class PersonBlock(blocks.StructBlock):
    name = blocks.CharBlock()
    job = blocks.CharBlock(required=False)
    institution = blocks.CharBlock(required=False)
    url = blocks.URLBlock(required=False)
    photo = ImageChooserBlock(required=False)

    class Meta:
        icon = 'person'
        template = 'public/blocks/person.html'
