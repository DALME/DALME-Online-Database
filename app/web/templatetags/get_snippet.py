"""Templatetag to return snippet."""

from django import template

register = template.Library()


@register.simple_tag()
def get_snippet(obj, width):
    """Return snippet of passed object to the passed width."""
    return obj.snippet(width)
