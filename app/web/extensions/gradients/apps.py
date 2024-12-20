"""Apps module for gradients extension."""

from django.apps import AppConfig


class GradientsAppConfig(AppConfig):
    name = 'web.extensions.gradients'
    label = 'webgradients'
    verbose_name = 'IDA Gradients Module'
