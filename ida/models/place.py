"""Place model."""

from django.db import models
from django.db.models import options

from ida.models.abstract import TrackingMixin, UuidMixin
from ida.models.attribute import AttributeMixin
from ida.models.comment import CommentMixin
from ida.models.entity import AttestationMixin
from ida.models.tag import TagMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Place(UuidMixin, TrackingMixin, AttestationMixin, AttributeMixin, CommentMixin, TagMixin):
    """Stores place information."""

    name = models.CharField(max_length=255)
    location = models.ForeignKey('ida.Location', on_delete=models.SET_NULL, null=True)

    objects = models.Manager()
