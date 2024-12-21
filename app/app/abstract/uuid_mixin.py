"""Mixin that assigns a unique uuid4 to a model instance."""

import uuid

from django.db import models


class UuidMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)

    class Meta:
        abstract = True
