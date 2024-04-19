"""Apps module for records extension."""

from django.apps import AppConfig


class RecordsAppConfig(AppConfig):
    name = 'public.extensions.records'
    label = 'publicrecords'
    verbose_name = 'IDA Records Module'
