"""Hooks for analytics extension."""

from wagtail import hooks

from django.templatetags.static import static
from django.utils.html import format_html


@hooks.register('register_icons')
def register_extra_icons(icons):
    return [
        *icons,
        'icons/plausible.svg',
    ]


@hooks.register('insert_global_admin_css')
def extra_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('css/analytics-admin.css'),
    )
