"""Configure the domain application."""

from django.apps import AppConfig


class DomainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'domain'

    def ready(self):
        import domain.signals  # noqa: F401
