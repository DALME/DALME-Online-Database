"""Saved search model."""

from django.db import models
from django.db.models import options

from ida.models.templates import IDAOwned, IDAUuid
from ida.models.tenant_scoped import ScopedBase

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class SavedSearch(ScopedBase, IDAUuid, IDAOwned):
    """Stores saved searches."""

    name = models.CharField(max_length=255)
    search = models.JSONField()
