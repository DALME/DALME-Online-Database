"""Saved search model."""

from django.db import models
from django.db.models import options

from ida.models.templates import OwnedMixin, TrackedMixin, UuidMixin
from ida.models.tenant_scoped import ScopedBase

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class SavedSearch(ScopedBase, UuidMixin, TrackedMixin, OwnedMixin):
    """Stores saved searches."""

    name = models.CharField(max_length=255)
    shareable = models.BooleanField(default=False)
    search = models.JSONField()
