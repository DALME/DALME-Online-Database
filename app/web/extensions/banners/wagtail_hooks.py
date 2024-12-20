"""Hooks for banners extension."""

from wagtail import hooks

from .views import BannersViewSet

hooks.register('register_admin_viewset', BannersViewSet)


@hooks.register('register_icons')
def register_extra_icons(icons):
    return [
        *icons,
        'wagtailfontawesomesvg/solid/bullhorn.svg',
    ]
