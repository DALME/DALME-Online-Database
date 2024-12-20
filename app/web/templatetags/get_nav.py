"""Templatetag to return nav links."""

from django import template

from web.models import (
    Home,
)

register = template.Library()


@register.simple_tag
def get_nav():
    home = Home.objects.first()
    return [page.specific for page in (home, *home.get_children().live().filter(show_in_menus=True))]
