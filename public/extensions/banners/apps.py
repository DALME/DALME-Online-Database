"""Apps module for banners extension."""

from django.apps import AppConfig


class BannersAppConfig(AppConfig):
    name = 'public.extensions.banners'
    label = 'publicbanners'
    verbose_name = 'IDA Banners Module'
