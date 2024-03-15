"""Templatetags to return header image style."""

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_header_image_styles(context, header_image, header_position):
    gradients = {
        'DALME': '125deg, rgba(6, 78, 140, 0.5) 0%, rgba(17, 74, 40, 0.5) 100%',
        'project': '125deg, rgba(83, 134, 160, 0.7) 0%, rgba(63, 101, 68, 0.9) 100%',
        'features': '125deg, rgba(99, 98, 58, 0.7) 0%, rgba(138, 71, 71, 0.9) 100%',
        'collections': '125deg, rgba(95, 81, 111, 0.7) 0%, rgba(23, 62, 101, 0.9) 100%',
        'about': '125deg, rgba(105, 102, 63, 0.6) 0%, rgba(146, 106, 16, 0.9) 100%',
        'generic': '59deg, #11587c 54.62%, #1b1b1b',
    }
    page = context['page']
    value = False
    count = 0

    while not value and count < 4:  # noqa: PLR2004
        value = gradients.get(page.slug, False)
        page = page.get_parent()

    if not value:
        value = gradients['generic']

    gradient = f'linear-gradient({value})'
    background_image = f'background-image: {gradient}, url({header_image.url})'
    return f'{background_image}; background-size: cover; background-position-y: {header_position}; width: 100%;'
