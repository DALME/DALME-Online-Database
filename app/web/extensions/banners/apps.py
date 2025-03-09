"""Apps module for banners extension."""

from django.apps import AppConfig


class BannersAppConfig(AppConfig):
    name = 'web.extensions.banners'
    label = 'webbanners'
    verbose_name = 'IDA Banners Module'
