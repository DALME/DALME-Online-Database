"""Make extra icons from Font Awesome SVG set available."""

from wagtail import hooks


@hooks.register('register_icons')
def register_extra_icons(icons):
    return [
        *icons,
        'wagtailfontawesomesvg/solid/notes-medical.svg',
        'wagtailfontawesomesvg/solid/book-bookmark.svg',
        'wagtailfontawesomesvg/solid/person.svg',
        'wagtailfontawesomesvg/solid/square-share-nodes.svg',
        'wagtailfontawesomesvg/solid/hand-holding-heart.svg',
        'wagtailfontawesomesvg/solid/diagram-successor.svg',
        'wagtailfontawesomesvg/solid/diagram-next.svg',
        'wagtailfontawesomesvg/solid/list-ol.svg',
        'wagtailfontawesomesvg/regular/bookmark.svg',
        'wagtailfontawesomesvg/solid/bandage.svg',
    ]
