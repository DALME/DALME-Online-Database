"""Locale reference model."""

from django.db import models
from django.db.models import options

from ida.models.utils import TrackingMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db', 'attribute_matching_fields')


class LocaleReference(TrackingMixin):
    """Stores information about geographic locales."""

    name = models.CharField(max_length=255)
    administrative_region = models.CharField(max_length=255)
    country = models.ForeignKey('ida.CountryReference', on_delete=models.SET_NULL, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    class Meta:
        ordering = ['country', 'name']
        unique_together = ('name', 'administrative_region')
        attribute_matching_fields = ['name', 'administrative_region', 'country']

    def __str__(self):
        return f'{self.name}, {self.administrative_region}, {self.country!s}'

    @property
    def detail(self):
        return f'{self.administrative_region}, {self.country!s}'

    def get_url(self):
        """Return url for instance."""
        return f'/locales/{self.id}'
