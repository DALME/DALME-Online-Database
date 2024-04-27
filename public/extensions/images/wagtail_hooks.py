"""Hooks for images extension."""

from wagtail import hooks


@hooks.register('register_icons')
def register_extra_icons(icons):
    return [
        *icons,
        'wagtailfontawesomesvg/solid/panorama.svg',
        'wagtailfontawesomesvg/solid/images.svg',
        'wagtailfontawesomesvg/solid/photo-film.svg',
    ]
