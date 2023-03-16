"""Model place data."""
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from dalme_app.models.templates import dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Place(dalmeUuid):
    """Stores place information."""

    name = models.CharField(max_length=255)
    attributes = GenericRelation('Attribute')
    instances = GenericRelation('EntityPhrase')
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    comments = GenericRelation('Comment')
    tags = GenericRelation('Tag')

    @property
    def comment_count(self):
        """Return count of comments."""
        return self.comments.count()
