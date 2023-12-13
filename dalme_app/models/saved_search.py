"""Model saved search data."""
from django.db import models
from django.db.models import options

from ida.models.templates import dalmeOwned, dalmeUuid

from .scoped import ScopedBase

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class SavedSearch(ScopedBase, dalmeUuid, dalmeOwned):
    """Stores saved searches."""

    name = models.CharField(max_length=255)
    search = models.JSONField()
