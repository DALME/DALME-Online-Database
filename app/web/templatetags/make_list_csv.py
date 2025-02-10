"""Templatetag that returns a list when passed a comma-delimited string."""

from django import template

register = template.Library()


@register.filter
def make_list_csv(obj):
    return obj.split(',')
