"""Templatetag that returns a comma-separated string when passed a list. If an additional parameter is passed it will be used as key to extract values from a list of dictionaries."""

from django import template

register = template.Library()


@register.filter
def get_string_list(lst, key=None):
    if not lst:
        return None
    return ', '.join([i[key] for i in lst]) if key else ', '.join([str(i) for i in lst])
