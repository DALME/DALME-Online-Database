"""Configure the app application."""

from django.apps import AppConfig


class IDAAppConfig(AppConfig):
    name = 'app'

    def ready(self):
        # Configures structlog and connects its request signals, which nothing
        # else imports.
        import app.logging  # noqa: F401
