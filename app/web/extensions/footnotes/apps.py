"""Apps module for footnotes extension."""

from django.apps import AppConfig


class FootnotesAppConfig(AppConfig):
    name = 'web.extensions.footnotes'
    label = 'webfootnotes'
    verbose_name = 'IDA Footnotes Module'
