"""Place model."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import TrackedMixin, UuidMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Place(UuidMixin, TrackedMixin):
    """Stores place information."""

    name = models.CharField(max_length=255)
    attributes = GenericRelation('ida.Attribute')
    instances = GenericRelation('ida.EntityPhrase')
    location = models.ForeignKey('ida.Location', on_delete=models.SET_NULL, null=True)
    comments = GenericRelation('ida.Comment')
    tags = GenericRelation('ida.Tag')

    @property
    def comment_count(self):
        """Return count of comments."""
        return self.comments.count()
