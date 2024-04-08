"""Apps module for gradients extension."""

from django.apps import AppConfig


class GradientsAppConfig(AppConfig):
    name = 'public.extensions.gradients'
    label = 'publicgradients'
    verbose_name = 'IDA Gradients Module'
