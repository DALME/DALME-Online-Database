"""Utilities to provide convenient context information throught the apps.

We can't define this in utils/middleware because the import tree is getting
quite complex and brittle at this point and it breaks start-up trying to import
everything in the utils module which includes lots of models that are not yet
loaded. So just put this at the top-level so it's clean and ready for use.

"""

from django_currentuser.middleware import get_current_user

from django.apps import apps
from django.contrib.contenttypes.models import ContentType


def get_gradient_pages():
    models = [
        m
        for m in apps.get_app_config('web').get_models()
        if any(f.name == 'gradient' for f in m._meta.get_fields())  # noqa: SLF001
    ]
    return [ct.id for ct in ContentType.objects.get_for_models(*models).values()]


def get_biblio_pages():
    model = apps.get_model('web', 'Bibliography')
    return [(p.id, p.short_title or p.title) for p in model.objects.all()]


def get_current_tenant():
    """Defer importing the tenant context to minimize impact on import resolution."""
    from tenants.middleware import TENANT

    return TENANT


def get_current_username():
    """Return current user's name."""
    return get_current_user().username
