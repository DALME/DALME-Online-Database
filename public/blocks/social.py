"""Block for showing social media links."""

from wagtail import blocks


class SocialBlock(blocks.StructBlock):
    fa_icon = blocks.CharBlock()
    url = blocks.URLBlock(required=False)
    css_class = blocks.CharBlock(required=False)

    class Meta:
        icon = 'group'
        template = 'public/blocks/social.html'
