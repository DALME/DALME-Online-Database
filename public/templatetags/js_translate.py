"""Templatetag to return valid js values."""

from django import template

register = template.Library()


@register.filter
def js_translate(value, mode=None):
    """Return javascript valid translation of passed value."""
    if mode == 'bool':
        return 'true' if value else 'false'
    if value is None:
        return 'null'
    if value is False:
        return 'false'
    if value is True:
        return 'true'
    if (
        type(value) in [int, list, dict]
        or value.startswith('"')
        and value.endswith('"')
        or value.startswith("'")
        and value.endswith("'")
    ):
        return value
    return value if value.startswith('"') and value.endswith('"') else f'"{value}"'
