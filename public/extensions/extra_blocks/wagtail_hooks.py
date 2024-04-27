"""Hooks for extra blocks extension."""

from wagtail import hooks


@hooks.register('register_icons')
def register_extra_icons(icons):
    return [
        *icons,
        'icons/expandable-text.svg',
        'wagtailfontawesomesvg/solid/chart-area.svg',
        'wagtailfontawesomesvg/solid/file-pdf.svg',
    ]
