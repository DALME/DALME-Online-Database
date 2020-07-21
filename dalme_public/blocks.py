from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class CarouselBlock(blocks.ListBlock):
    class Meta:
        icon = 'cogs'
        template = 'dalme_public/blocks/_carousel.html'


class DocumentBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    abstract = blocks.CharBlock()
    version = blocks.FloatBlock(required=False)
    document = DocumentChooserBlock(required=False)
    url = blocks.URLBlock(required=False)
    date = blocks.DateBlock()

    class Meta:
        icon = 'doc-full'
        template = 'dalme_public/blocks/_document.html'


class FooterPageChooserBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    page = blocks.PageChooserBlock()

    class Meta:
        icon = 'doc-full'
        template = 'dalme_public/blocks/_footer_page.html'


class ExternalResourceBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    info = blocks.CharBlock()
    url = blocks.URLBlock()
    date = blocks.DateBlock()

    class Meta:
        icon = 'link'
        template = 'dalme_public/blocks/_external_resource.html'


class MainImageBlock(ImageChooserBlock):
    class Meta:
        icon = 'image'
        template = 'dalme_public/blocks/_main_image.html'


class PersonBlock(blocks.StructBlock):
    name = blocks.CharBlock()
    job = blocks.CharBlock()
    institution = blocks.CharBlock()
    url = blocks.URLBlock(required=False)
    photo = ImageChooserBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'dalme_public/blocks/_person.html'


class SocialBlock(blocks.StructBlock):
    fa_icon = blocks.CharBlock()
    url = blocks.URLBlock()

    class Meta:
        icon = 'group'
        template = 'dalme_public/blocks/_social.html'


class SponsorBlock(blocks.StructBlock):
    logo = ImageChooserBlock()
    url = blocks.URLBlock()

    class Meta:
        icon = 'user'
        template = 'dalme_public/blocks/_sponsor.html'


class SubsectionBlock(blocks.StructBlock):
    subsection = blocks.CharBlock()
    collapsed = blocks.BooleanBlock(required=False, default=True)

    class Meta:
        icon = 'collapse-up'
        template = 'dalme_public/blocks/_subsection.html'
