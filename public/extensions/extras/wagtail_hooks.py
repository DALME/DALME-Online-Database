"""Hooks for extra blocks extension."""

from wagtail import hooks

from django.templatetags.static import static
from django.utils.html import format_html


@hooks.register('register_icons')
def register_extra_icons(icons):
    return [
        *icons,
        'icons/expandable-text.svg',
        'wagtailfontawesomesvg/solid/chart-area.svg',
        'wagtailfontawesomesvg/solid/file-pdf.svg',
        'wagtailfontawesomesvg/solid/table-cells.svg',
    ]


@hooks.register('insert_global_admin_css')
def extra_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('css/extras-admin.css'))
