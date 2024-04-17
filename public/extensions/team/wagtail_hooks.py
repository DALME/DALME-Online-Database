"""Hooks for team extension."""

from wagtail import hooks

from django.templatetags.static import static
from django.utils.html import format_html

from .views import TeamViewSetGroup

hooks.register('register_admin_viewset', TeamViewSetGroup)


@hooks.register('insert_global_admin_css')
def extra_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('css/team-admin.css'))
