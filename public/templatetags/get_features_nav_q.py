"""Templatetag to return querystring qualified by featured resource type."""

from django import template

register = template.Library()


@register.simple_tag()
def get_features_nav_q(key):
    return {
        'essays': '?kind=essay',
        'inventories': '?kind=inventory',
        'objects': '?kind=object',
    }[key]
