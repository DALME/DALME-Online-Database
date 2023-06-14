from django.db import models
from django.db.models import options

from dalme_app.models.templates import dalmeOwned, dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class SavedSearch(dalmeUuid, dalmeOwned):
    """Stores saved searches."""

    name = models.CharField(max_length=255)
    search = models.JSONField()
