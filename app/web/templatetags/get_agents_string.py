"""Templatetag that gets a list of Agent objects and returns a formatted string with their names."""

from django import template

register = template.Library()


@register.filter
def get_agents_string(obj):
    if not obj:
        return None
    names = [i['name'] for i in obj if i.get('name')]
    return ' ,'.join(names)
