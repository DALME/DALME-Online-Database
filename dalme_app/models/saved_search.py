from django.db import models
from dalme_app.models._templates import dalmeUuidOwned
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class SavedSearch(dalmeUuidOwned):
    name = models.CharField(max_length=255)
    search = models.JSONField()
