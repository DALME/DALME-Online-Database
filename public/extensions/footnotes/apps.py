"""Apps module for footnotes extension."""

from django.apps import AppConfig


class FootnotesAppConfig(AppConfig):
    name = 'public.extensions.footnotes'
    label = 'publicfootnotes'
    verbose_name = 'IDA Footnotes Module'
