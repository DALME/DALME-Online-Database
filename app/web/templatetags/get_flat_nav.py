"""Templatetag to return nav for flat pages."""

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_flat_nav(context):
    page = context['page']
    target = page if page.show_in_menus else page.get_parent()
    return [p.specific for p in target.get_siblings().live().filter(show_in_menus=True)]
