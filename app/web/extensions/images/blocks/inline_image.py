"""Inline image block."""

from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.images.blocks import ImageChooserBlock
from wagtail.telepath import register

from django import forms
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

from web.extensions.extras.widgets import CustomSelect


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


class InlineImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(
        required=True,
        help_text='Select the image to display.',
    )
    image_id = blocks.CharBlock(
        required=False,
        label='Image ID',
        help_text='String to use as link anchor.',
    )
    show_caption = blocks.BooleanBlock(
        required=False,
        default=True,
        label='Caption',
        help_text='Render caption?',
    )
    use_file_caption = blocks.BooleanBlock(
        required=False,
        default=True,
        label='Caption from file',
        help_text='Uncheck to write caption.',
    )
    caption = blocks.RichTextBlock(editor='minimal', required=False, label='Caption text')
    alignment = blocks.ChoiceBlock(
        choices=[
            ('left', 'Left-aligned'),
            ('right', 'Right-aligned'),
            ('centre', 'Centre-aligned'),
            ('main', 'Main image (full-width)'),
        ],
        default='left',
        widget=CustomSelect,
        help_text='How should the image be aligned on the page?',
    )
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
        widget=CustomSelect,
        required=False,
        help_text='Resize using a <a href="https://docs.wagtail.org/en/v2.13.5/topics/images.html" target="_blank">built-in rule</a>\
            or use as background of &lt;div&gt; with fixed dimensions.',
    )
    dimensions = blocks.CharBlock(
        required=False,
        validators=[validate_dimensions],
        help_text='Width x height, e.g. "400x200".',
    )
    parameters = blocks.CharBlock(
        required=False,
        label='CSS parameters',
        help_text='CSS parameters to be used if the image is displayed as a background, e.g. "no-repeat top/cover".',
    )

    class Meta:
        icon = 'images'
        template = 'images/inline_image_block.html'
        form_classname = 'struct-block inline-image-block'
        form_template = 'images/inline_image_form.html'
        label_format = 'Inline image {image_id}'


class InlineImageBlockAdapter(StructBlockAdapter):
    js_constructor = 'webimage.InlineImageBlock'

    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(
            js=[*structblock_media._js, 'js/inline-image-form.js'],  # noqa: SLF001
            css={'all': ['css/inline-image-form.css']},
        )


register(InlineImageBlockAdapter(), InlineImageBlock)
