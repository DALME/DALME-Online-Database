"""WSGI config for shariasource.hub.app.

It exposes the WSGI callable as a module-level variable named `application`.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/

"""

from configurations.wsgi import get_wsgi_application

from django.conf import settings
from django.db.backends.signals import connection_created
from django.dispatch import receiver

application = get_wsgi_application()


@receiver(connection_created)
def setup_postgres(connection, **kwargs):  # noqa: ARG001
    """Set a global timeout on Django SQL queries.

    By setting it here it only affects queries on the wsgi pathway, ie. worker
    processes.

    """
    if connection.vendor != 'postgresql':
        return

    # Timeout statements after 30 seconds.
    with connection.cursor() as cursor:
        cursor.execute('SET statement_timeout TO %s;', [settings.SQL_TIMEOUT])
