"""Hooks for banners extension."""

from wagtail import hooks

from .views import BannersViewSet

hooks.register('register_admin_viewset', BannersViewSet)
