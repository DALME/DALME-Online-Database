"""Mixin that allows attributes to be attached to a model instance."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class AttributeMixin(models.Model):
    attributes = GenericRelation(
        'ida.Attribute',
        related_query_name='%(app_label)s_%(class)s_related',
    )

    class Meta:
        abstract = True

    @property
    def attribute_count(self):
        """Return count of attributes."""
        return self.attributes.count()
