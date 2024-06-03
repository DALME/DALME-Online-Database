"""Place model."""

from django.db import models
from django.db.models import options

from ida.models.utils import AttestationMixin, CommentMixin, TaggingMixin, TrackingMixin, UuidMixin
from ida.models.utils.attribute_mixin import AttributeMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Place(UuidMixin, TrackingMixin, AttestationMixin, AttributeMixin, CommentMixin, TaggingMixin):
    """Stores place information."""

    name = models.CharField(max_length=255)
    location = models.ForeignKey('ida.Location', on_delete=models.SET_NULL, null=True)
