from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class DocumentBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    abstract = blocks.CharBlock()
    version = blocks.FloatBlock()
    document = DocumentChooserBlock()
    date = blocks.DateBlock()

    class Meta:
        icon = 'doc-full'
        template = 'dalme_public/blocks/_document.html'


class ExternalResourceBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    info = blocks.CharBlock()
    url = blocks.URLBlock()
    date = blocks.DateBlock()

    class Meta:
        icon = 'link'
        template = 'dalme_public/blocks/_external_resource.html'


class IFrameBlock(blocks.RawHTMLBlock):
    class Meta:
        label = 'Iframe'
        icon = 'code'


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


class SubsectionBlock(blocks.StructBlock):
    subsection = blocks.CharBlock()
    collapsed = blocks.BooleanBlock(required=False, default=True)

    class Meta:
        icon = 'collapse-up'
        template = 'dalme_public/blocks/_subsection.html'
