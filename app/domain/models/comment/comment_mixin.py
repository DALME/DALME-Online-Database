"""Mixin that allows comments to be attached to a model instance."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class CommentMixin(models.Model):
    comments = GenericRelation(
        'domain.Comment',
        related_query_name='%(app_label)s_%(class)s_related',
    )

    class Meta:
        abstract = True

    @property
    def comment_count(self):
        """Return count of comments."""
        return self.comments.count()
