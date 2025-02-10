"""Mixin for assigning permissions to model instances."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class PermissionMixin(models.Model):
    permissions = GenericRelation(
        'domain.Permission',
        related_query_name='%(app_label)s_%(class)s_related',
    )

    class Meta:
        abstract = True
