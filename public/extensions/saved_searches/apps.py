"""Apps module for saved searches extension."""

from django.apps import AppConfig


class SavedSearchesAppConfig(AppConfig):
    name = 'public.extensions.saved_searches'
    verbose_name = 'IDA Saved Searches Module'
