"""Templatetag to return classname of object."""

from django import template

register = template.Library()


@register.filter
def classname(obj):
    """Return classname of passed object."""
    return obj.specific.__class__.__name__
