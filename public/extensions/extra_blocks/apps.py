"""Apps module for extra_blocks extension."""

from django.apps import AppConfig


class ExtraBlocksAppConfig(AppConfig):
    name = 'public.extensions.extra_blocks'
    label = 'publicextrablocks'
    verbose_name = 'IDA Extra Blocks Module'
