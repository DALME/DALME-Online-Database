"""Hooks for announcement extension."""

from wagtail import hooks

from .views import AnnouncementsViewSet

hooks.register('register_admin_viewset', AnnouncementsViewSet)
