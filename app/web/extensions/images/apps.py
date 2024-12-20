"""Apps module for images extension."""

from django.apps import AppConfig


class ImagesAppConfig(AppConfig):
    name = 'web.extensions.images'
    label = 'webimages'
    verbose_name = 'IDA Images Module'
