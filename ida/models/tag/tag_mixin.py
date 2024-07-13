"""Mixin that allows tags to be attached to a model instance."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class TagMixin(models.Model):
    tags = GenericRelation(
        'ida.Tag',
        related_query_name='%(app_label)s_%(class)s_related',
    )

    class Meta:
        abstract = True

    @property
    def tag_count(self):
        """Return count of tags."""
        return self.tags.count()
