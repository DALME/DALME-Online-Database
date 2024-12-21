"""Location model."""

from django.db import models
from django.db.models import options

from app.abstract import TrackingMixin, UuidMixin
from domain.models.attribute import AttributeMixin
from domain.models.comment import CommentMixin
from domain.models.tag import TagMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Location(UuidMixin, TrackingMixin, AttributeMixin, CommentMixin, TagMixin):
    """Stores location information."""

    ADDRESS = 1
    COUNTRY = 2
    GEOMETRY = 3
    LOCALE = 4
    LOCATION_TYPES = (
        (ADDRESS, 'Address'),
        (COUNTRY, 'Country'),
        (GEOMETRY, 'Geometry'),
        (LOCALE, 'Locale'),
    )

    location_type = models.IntegerField(choices=LOCATION_TYPES)

    objects = models.Manager()
