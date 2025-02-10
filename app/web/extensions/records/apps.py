"""Apps module for records extension."""

from django.apps import AppConfig


class RecordsAppConfig(AppConfig):
    name = 'web.extensions.records'
    label = 'webrecords'
    verbose_name = 'IDA Records Module'
