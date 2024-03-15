"""Templatetag for rendering images."""

from django import template

register = template.Library()


@register.simple_tag()
def render_image(record):
    image = record.get('image')
    resize_rule = record.get('resize_rule')
    dimensions = record.get('dimensions')
    image_id = record.get('image_id')
    parameters = record.get('parameters')
    img = (
        image.get_rendition(f'{resize_rule}-{dimensions}')
        if resize_rule and resize_rule != 'background'
        else image.get_rendition('original')
    )
    img_tag = f'<img alt="{img.alt}" height="{img.height}" width="{img.width}" src="{img.url}" '
    img_tag = img_tag + f'id="{image_id}" ' if image_id and resize_rule != 'background' else img_tag
    img_tag = img_tag + 'class="display-none" ' if resize_rule == 'background' else img_tag
    img_tag += '/>'

    if resize_rule == 'background':
        width, height = dimensions.split('x')
        width = width if int(width) < 308 else 308  # noqa: PLR2004
        div_tag = '<div class="image-as-background" '
        div_tag = div_tag + f'id="{image_id}" '
        div_tag += f'style="background: url({img.url}) {parameters}; width: {width}px; height: {height}px;"></div>'

    return img_tag + div_tag if resize_rule == 'background' else img_tag
