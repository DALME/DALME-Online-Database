"""Model place data."""
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Place(dalmeUuid):
    """Stores place information."""

    name = models.CharField(max_length=255)
    attributes = GenericRelation('dalme_app.Attribute')
    instances = GenericRelation('dalme_app.EntityPhrase')
    location = models.ForeignKey('dalme_app.Location', on_delete=models.SET_NULL, null=True)
    comments = GenericRelation('dalme_app.Comment')
    tags = GenericRelation('dalme_app.Tag')

    @property
    def comment_count(self):
        """Return count of comments."""
        return self.comments.count()
