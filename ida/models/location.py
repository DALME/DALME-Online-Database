"""Location model."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import TrackedMixin, UuidMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Location(UuidMixin, TrackedMixin):
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
    attributes = GenericRelation('ida.Attribute')
    comments = GenericRelation('ida.Comment')
    tags = GenericRelation('ida.Tag')

    @property
    def comment_count(self):
        """Return count of comments."""
        return self.comments.count()
