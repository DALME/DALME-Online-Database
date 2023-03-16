"""Define custom CMS blocks."""
from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class AnnouncementBannerBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    info = blocks.TextBlock()
    page = blocks.PageChooserBlock(required=False)
    url = blocks.URLBlock(required=False)
    start_date = blocks.DateBlock()
    end_date = blocks.DateBlock()

    class Meta:
        icon = 'media'
        template = 'dalme_public/blocks/_announcement_banner.html'


class BibliographyBlock(blocks.StructBlock):
    collection = blocks.ChoiceBlock(
        choices=[
            ('A4QHN348', 'Editions'),
            ('BKW2PVCM', 'Glossaries and dictionaries'),
            ('QM9AZNT3', 'Methodology'),
            ('SLIT6LID', 'Studies'),
            ('FRLVXUWL', 'Other resources'),
        ],
    )

    class Meta:
        icon = 'list-ul'
        template = 'dalme_public/blocks/_bibliography.html'


class CarouselBlock(blocks.ListBlock):
    class Meta:
        icon = 'cogs'
        template = 'dalme_public/blocks/_carousel.html'


class ChartEmbedBlock(blocks.StructBlock):
    html = blocks.RawHTMLBlock()
    alignment = blocks.ChoiceBlock(
        choices=[
            ('left', 'Left-aligned'),
            ('right', 'Right-aligned'),
            ('full', 'Full-width'),
        ],
    )

    class Meta:
        icon = 'image'
        template = 'dalme_public/blocks/_chart_embed.html'


class DocumentBlock(blocks.StructBlock):
    type = blocks.ChoiceBlock(  # noqa: A003
        choices=[
            ('document', 'Document'),
            ('publication', 'Publication'),
            ('talk', 'Talk'),
        ],
    )
    title = blocks.CharBlock()
    abstract = blocks.CharBlock(required=False)
    author = blocks.CharBlock()
    detail = blocks.CharBlock(required=False)
    version = blocks.FloatBlock(required=False)
    document = DocumentChooserBlock(required=False)
    url = blocks.URLBlock(required=False)
    page = blocks.PageChooserBlock(required=False)
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


class InlineImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.RichTextBlock(required=False)
    alignment = blocks.ChoiceBlock(
        choices=[
            ('left', 'Left-aligned'),
            ('right', 'Right-aligned'),
        ],
    )
    show_caption = blocks.BooleanBlock(required=False, default=True)

    class Meta:
        icon = 'image'
        template = 'dalme_public/blocks/_inline_image.html'


class PersonBlock(blocks.StructBlock):
    name = blocks.CharBlock()
    job = blocks.CharBlock(required=False)
    institution = blocks.CharBlock(required=False)
    url = blocks.URLBlock(required=False)
    photo = ImageChooserBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'dalme_public/blocks/_person.html'


class SocialBlock(blocks.StructBlock):
    fa_icon = blocks.CharBlock()
    url = blocks.URLBlock(required=False)
    css_class = blocks.CharBlock(required=False)

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
    minor_heading = blocks.BooleanBlock(required=False, default=False)

    class Meta:
        icon = 'collapse-down'
        template = 'dalme_public/blocks/_subsection.html'


class SubsectionEndMarkerBlock(blocks.StructBlock):
    class Meta:
        icon = 'collapse-up'
        template = 'dalme_public/blocks/_subsection_end.html'
