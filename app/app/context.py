"""Utilities to provide convenient context information throught the apps.

We can't define this in utils/middleware because the import tree is getting
quite complex and brittle at this point and it breaks start-up trying to import
everything in the utils module which includes lots of models that are not yet
loaded. So just put this at the top-level so it's clean and ready for use.

"""

import contextvars

from django_currentuser.middleware import get_current_user

from django.apps import apps
from django.contrib.contenttypes.models import ContentType

_gradient_pages = contextvars.ContextVar('gradient_pages', default=[])
_biblio_pages = contextvars.ContextVar('biblio_pages', default=[])


def get_gradient_pages():
    if not _gradient_pages.get():
        app_config = apps.get_app_config('public')
        if app_config.models_module is not None:
            models = [
                m.__name__.lower()
                for m in app_config.get_models()
                if any(f.name == 'gradient' for f in m._meta.get_fields())  # noqa: SLF001
            ]
            _gradient_pages.set([ct.id for ct in ContentType.objects.filter(app_label='public', model__in=models)])
    return _gradient_pages.get()


def get_biblio_pages():
    if not _biblio_pages.get():
        model = apps.get_model('public', 'Bibliography')
        _biblio_pages.set([(p.id, p.short_title if p.short_title else p.title) for p in model.objects.all()])
    return _biblio_pages.get()


def get_current_tenant():
    """Defer importing the tenant context to minimize impact on import resolution."""
    from app.middleware import TENANT

    return TENANT


def get_current_username():
    """Return current user's name."""
    return get_current_user().username
