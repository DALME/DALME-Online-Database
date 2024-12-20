"""Place model."""

from django.db import models
from django.db.models import options

from domain.models.abstract import TrackingMixin, UuidMixin
from domain.models.attribute import AttributeMixin
from domain.models.comment import CommentMixin
from domain.models.entity import AttestationMixin
from domain.models.tag import TagMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Place(UuidMixin, TrackingMixin, AttestationMixin, AttributeMixin, CommentMixin, TagMixin):
    """Stores place information."""

    name = models.CharField(max_length=255)
    location = models.ForeignKey('domain.Location', on_delete=models.SET_NULL, null=True)

    objects = models.Manager()
