"""Apps module for bibliography extension."""

from django.apps import AppConfig


class BibliographyAppConfig(AppConfig):
    name = 'public.extensions.bibliography'
    label = 'publicbibliography'
    verbose_name = 'IDA Bibliography Module'
