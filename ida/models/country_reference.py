"""Country reference model."""

from django.db import models
from django.db.models import options

from ida.models.utils import TrackingMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db', 'attribute_matching_fields')


class CountryReference(TrackingMixin):
    """Stores country information."""

    name = models.CharField(max_length=255, unique=True)
    alpha_3_code = models.CharField(max_length=3)
    alpha_2_code = models.CharField(max_length=2)
    num_code = models.IntegerField()

    class Meta:
        ordering = ['name']
        attribute_matching_fields = ['name']

    def __str__(self):
        return self.name

    def get_url(self):
        """Return url for instance."""
        return f'/countries/{self.id}'
