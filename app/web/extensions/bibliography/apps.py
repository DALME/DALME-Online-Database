"""Apps module for bibliography extension."""

from django.apps import AppConfig


class BibliographyAppConfig(AppConfig):
    name = 'web.extensions.bibliography'
    label = 'webbibliography'
    verbose_name = 'IDA Bibliography Module'
