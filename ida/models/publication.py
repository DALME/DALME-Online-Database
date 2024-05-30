"""Publication model."""

from django.db import models
from django.db.models import options

from ida.models.utils import (
    AttributeMixin,
    CommentMixin,
    PermissionsMixin,
    TaggingMixin,
    TrackingMixin,
    UuidMixin,
)

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Publication(UuidMixin, TrackingMixin, AttributeMixin, CommentMixin, PermissionsMixin, TaggingMixin):
    """Stores information about publications."""

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
