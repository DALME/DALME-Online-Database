"""Publication model."""

from django.db import models
from django.db.models import options

from app.abstract import TrackingMixin, UuidMixin
from domain.models.attribute import AttributeMixin
from domain.models.comment import CommentMixin
from domain.models.permission import PermissionMixin
from domain.models.tag import TagMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db', 'attribute_matching_fields')


class Publication(UuidMixin, TrackingMixin, AttributeMixin, CommentMixin, PermissionMixin, TagMixin):
    """Stores information about publications."""

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)

    class Meta:
        attribute_matching_fields = ['name', 'short_name']
