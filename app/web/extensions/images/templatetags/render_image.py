"""Templatetag for rendering images."""

from django import template

from .sanitize_alt_text import sanitize_alt_text

register = template.Library()


@register.simple_tag
def render_image(record):
    image = record.get('image')
    resize_rule = record.get('resize_rule')
    dimensions = record.get('dimensions')
    image_id = record.get('image_id')
    parameters = record.get('parameters')
    is_main = record.get('alignment') == 'main'

    if is_main:
        img = image.get_rendition('fill-1000x350-c100')
    elif resize_rule and resize_rule != 'background':
        img = image.get_rendition(f'{resize_rule}-{dimensions}')
    else:
        img = image.get_rendition('original')

    img_tag = f'<img alt="{sanitize_alt_text(img.alt)}" height="{img.height}" width="{img.width}" src="{img.url}" '
    img_tag = img_tag + f'id="{image_id}" ' if image_id and resize_rule != 'background' else img_tag
    img_tag = img_tag + 'class="u-none" ' if resize_rule == 'background' else img_tag
    img_tag += '/>'

    if resize_rule == 'background':
        width, height = dimensions.split('x')
        width = width if int(width) < 308 else 308  # noqa: PLR2004
        div_tag = '<div class="image-as-background" '
        div_tag = div_tag + f'id="{image_id}" ' if image_id else div_tag
        div_tag += f'style="background: url({img.url}) {parameters}; width: {width}px; height: {height}px;"></div>'

    return img_tag + div_tag if resize_rule == 'background' else img_tag
