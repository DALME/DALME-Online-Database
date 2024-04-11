"""Templatetags to return header image style."""

from django import template

from ida.context import get_gradient_pages

register = template.Library()


@register.simple_tag(takes_context=True)
def get_header_image_styles(context, header_image, header_position):
    page = context['page']
    gradient = 'linear-gradient(59deg, #11587c 54.62%, #1b1b1b)'
    try:
        if hasattr(page, 'gradient'):
            gradient = page.gradient.css
        else:
            section = page.get_ancestors().filter(content_type_id__in=get_gradient_pages())
            if section.exists():
                gradient = section.last().specific_deferred.gradient.css
    except AttributeError:
        pass

    background_image = f'background-image: {gradient}, url({header_image.url})'
    return f'{background_image}; background-size: cover; background-position-y: {header_position}; width: 100%;'
