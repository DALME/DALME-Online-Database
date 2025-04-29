"""Templatetag to return snippet."""

import textwrap

from django import template

register = template.Library()


@register.simple_tag()
def get_snippet(target, width):
    """Return snippet of passed object or text to the passed width."""
    if isinstance(target, str):
        return textwrap.shorten(target, width=width, placeholder='...')
    return target.snippet(width)
