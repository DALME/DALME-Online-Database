"""Hooks for team extension."""

from wagtail import hooks

from .views import TeamViewSetGroup

hooks.register('register_admin_viewset', TeamViewSetGroup)
