"""Saved search model."""

from django.db import models
from django.db.models import options

from domain.models.abstract import OwnedMixin, TrackingMixin, UuidMixin
from domain.models.tenant import TenantMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class SavedSearch(TenantMixin, UuidMixin, TrackingMixin, OwnedMixin):
    """Stores saved searches."""

    name = models.CharField(max_length=255)
    shareable = models.BooleanField(default=False)
    search = models.JSONField()
