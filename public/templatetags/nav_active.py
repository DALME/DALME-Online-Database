"""Templatetags to return boolean indicating whether nav should be active."""

from django import template

from public.models import (
    Home,
)

register = template.Library()


@register.simple_tag(takes_context=True)
def nav_active(context, tab):
    page = context['page'].specific
    tab = tab.specific
    if page == tab:
        return True
    if not isinstance(tab, Home) and page in [desc.specific for desc in tab.get_descendants()]:
        return True
    return False
