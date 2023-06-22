from django.apps import AppConfig


class DalmeConfig(AppConfig):  # noqa: D101
    name = 'dalme_app'

    def ready(self):  # noqa: D102
        import dalme_app.signals  # noqa: F401
