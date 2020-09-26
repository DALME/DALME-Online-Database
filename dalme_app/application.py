from django.apps import AppConfig


class DalmeConfig(AppConfig):
    name = 'dalme_app'

    def ready(self):
        import dalme_app.signals
