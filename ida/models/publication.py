"""Publication model."""

from django.db import models
from django.db.models import options

from ida.models.abstract import TrackingMixin, UuidMixin
from ida.models.attribute import AttributeMixin
from ida.models.comment import CommentMixin
from ida.models.permission import PermissionMixin
from ida.models.tag import TagMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db', 'attribute_matching_fields')


class Publication(UuidMixin, TrackingMixin, AttributeMixin, CommentMixin, PermissionMixin, TagMixin):
    """Stores information about publications."""

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)

    class Meta:
        attribute_matching_fields = ['name', 'short_name']
