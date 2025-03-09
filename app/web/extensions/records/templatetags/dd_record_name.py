"""Templatetag to parse record name."""

from django import template

register = template.Library()


@register.filter
def dd_record_name(name, part=''):
    try:
        name_string = name.split('(')
        if part == 'loc':
            try:
                return name_string[1][:-1]
            except IndexError:
                return 'Archival location not available'
        return name_string[0]
    except AttributeError:
        return name
