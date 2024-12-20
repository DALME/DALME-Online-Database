"""Apps module for team extension."""

from django.apps import AppConfig


class TeamAppConfig(AppConfig):
    name = 'web.extensions.team'
    label = 'webteam'
    verbose_name = 'IDA Team Module'

    def ready(self):
        from . import signals  # noqa: F401
