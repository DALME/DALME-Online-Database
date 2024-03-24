"""Inline image block."""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from django.core.exceptions import ValidationError


def validate_dimensions(value):
    try:
        if 'x' in value:
            dims = value.split('x')
            if len(dims) != 2 or not dims[0].isdigit() or not dims[1].isdigit():  # noqa: PLR2004
                msg = 'Must be either a single integer or two integers separated by the letter "x".'
                raise ValidationError(msg)
        elif not value.isdigit():
            msg = 'Must be either a single integer or two integers separated by the letter "x".'
            raise ValidationError(msg)
    except Exception() as err:
        msg = 'Must be either a single integer or two integers separated by the letter "x".'
        raise ValidationError(msg) from err


class MainImageBlock(ImageChooserBlock):
    class Meta:
        icon = 'image'
        template = 'public/blocks/main_image.html'


class InlineImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    image_id = blocks.CharBlock(required=False, help_text='Can be used as an anchor to link to the image.')
    caption = blocks.RichTextBlock(required=False)
    alignment = blocks.ChoiceBlock(
        choices=[
            ('left', 'Left-aligned'),
            ('right', 'Right-aligned'),
        ],
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
        template = 'public/blocks/inline_image.html'
