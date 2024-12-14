from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from django.core.exceptions import ValidationError


def validate_dimensions(value):
    try:
        if 'x' in value:
            dims = value.split('x')
            if len(dims) != 2 or not dims[0].isdigit() or not dims[1].isdigit():
                raise ValidationError(f'Must be either a single integer or two integers separated by the letter "x".')
        else:
            if not value.isdigit():
                raise ValidationError(f'Must be either a single integer or two integers separated by the letter "x".')
    except:
        raise ValidationError(f'Must be either a single integer or two integers separated by the letter "x".')


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
        choices=[('left', 'Left-aligned'), ('right', 'Right-aligned'), ('full', 'Full-width')],
    )

    class Meta:
        icon = 'image'
        template = 'dalme_public/blocks/_chart_embed.html'


class DocumentBlock(blocks.StructBlock):
    type = blocks.ChoiceBlock(
        choices=[('document', 'Document'), ('publication', 'Publication'), ('talk', 'Talk')],
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
    image_id = blocks.CharBlock(required=False, help_text='Can be used as an anchor to link to the image.')
    caption = blocks.RichTextBlock(required=False)
    alignment = blocks.ChoiceBlock(
        choices=[('left', 'Left-aligned'), ('right', 'Right-aligned')],
    )
    show_caption = blocks.BooleanBlock(required=False, default=True)
    resize_rule = blocks.ChoiceBlock(
        choices=[
            ('max', 'Fit within the given dimensions'),
            ('min', 'Cover the given dimensions'),
            ('width', 'Reduce width to the given dimension'),
            ('height', 'Reduce height to the given dimension'),
            ('scale', 'Resize to the given percentage'),
            ('fill', 'Resize and crop to the given dimensions'),
            ('background', 'As background with given parameters'),
        ],
        required=False,
        help_text='Resize the image using one of <a href="https://docs.wagtail.org/en/v2.13.5/topics/images.html" target="_blank">Wagtail\'s built-in rules</a>\
            or use it as a background and style it with CSS. If the latter is chosen, the dimensions will be used to determine the size of the containing &lt;div&gt;.',
    )
    dimensions = blocks.CharBlock(
        required=False,
        validators=[validate_dimensions],
        help_text='Width and height separated by an "x", e.g. "400x200". The maximum allowed width for an inline image is 308px.',
    )
    parameters = blocks.CharBlock(
        required=False,
        help_text='CSS parameters to be used if the image is displayed as a background, e.g. "no-repeat top/cover".',
    )

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


class FootnotesPlaceMarker(blocks.StructBlock):
    class Meta:
        icon = 'list-ol'
        template = 'dalme_public/blocks/_footnote_placemarker.html'
