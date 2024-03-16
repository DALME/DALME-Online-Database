"""Templatetags to return header image style."""

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_header_image_styles(context, header_image, header_position):
    page = context['page']
    if hasattr(page, 'gradient'):
        gradient = page.gradient.css
    else:
        section = page.get_ancestors().filter(content_type_id__in=[118, 123, 126])
        if section.exists():
            gradient = section.first().specific_deferred.gradient.css
        else:
            gradient = 'linear-gradient(59deg, #11587c 54.62%, #1b1b1b)'

    background_image = f'background-image: {gradient}, url({header_image.url})'
    return f'{background_image}; background-size: cover; background-position-y: {header_position}; width: 100%;'
