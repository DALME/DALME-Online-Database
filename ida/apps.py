"""Configure the ida application."""

from django.apps import AppConfig


class IDAConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ida'

    def ready(self):
        import ida.signals  # noqa: F401
