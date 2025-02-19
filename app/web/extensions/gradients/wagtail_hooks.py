"""Hooks for gradients extension."""

from wagtail import hooks

from django.templatetags.static import static
from django.utils.html import format_html

from .views import GradientChooserViewSet, GradientViewSet

hooks.register('register_admin_viewset', GradientViewSet)
hooks.register('register_admin_viewset', GradientChooserViewSet)


@hooks.register('insert_global_admin_css')
def extra_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('web/extensions/gradients/css/gradient-chooser.css'),
    )


@hooks.register('register_icons')
def register_extra_icons(icons):
    return [
        *icons,
        'wagtailfontawesomesvg/solid/swatchbook.svg',
    ]
