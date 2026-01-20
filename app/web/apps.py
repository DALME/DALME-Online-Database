"""Configure the web application."""

from django.apps import AppConfig


class WebConfig(AppConfig):
    name = 'web'

    def ready(self):
        # Force eager resolution of default_storage.
        from django.core.files.storage import default_storage

        default_storage._setup()  # noqa: SLF001
