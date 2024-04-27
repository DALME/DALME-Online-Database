"""Apps module for images extension."""

from django.apps import AppConfig


class ImagesAppConfig(AppConfig):
    name = 'public.extensions.images'
    label = 'publicimages'
    verbose_name = 'IDA Images Module'
