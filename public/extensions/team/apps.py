"""Apps module for team extension."""

from django.apps import AppConfig


class TeamAppConfig(AppConfig):
    name = 'public.extensions.team'
    label = 'publicteam'
    verbose_name = 'IDA Team Module'
