"""Location model."""

from django.db import models
from django.db.models import options

from ida.models.utils import CommentMixin, TaggingMixin, TrackingMixin, UuidMixin
from ida.models.utils.attribute_mixin import AttributeMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Location(UuidMixin, TrackingMixin, AttributeMixin, CommentMixin, TaggingMixin):
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
