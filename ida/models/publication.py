"""Publication model."""

from django.db import models
from django.db.models import options

from ida.models.utils import (
    CommentMixin,
    PermissionsMixin,
    TaggingMixin,
    TrackingMixin,
    UuidMixin,
)
from ida.models.utils.attribute_mixin import AttributeMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db', 'attribute_matching_fields')


class Publication(UuidMixin, TrackingMixin, AttributeMixin, CommentMixin, PermissionsMixin, TaggingMixin):
    """Stores information about publications."""

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)

    class Meta:
        attribute_matching_fields = ['name', 'short_name']
