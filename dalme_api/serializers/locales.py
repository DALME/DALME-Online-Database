from dalme_app.models import LocaleReference

from .base_classes import DynamicSerializer
from .countries import CountryReferenceSerializer


class LocaleReferenceSerializer(DynamicSerializer):
    """Serializer for locales."""

    country = CountryReferenceSerializer(field_set='attribute')

    class Meta:  # noqa: D106
        model = LocaleReference
        fields = ('id', 'name', 'administrative_region', 'country', 'latitude', 'longitude')
        field_sets = {
            'option': ['id', 'name', 'country'],
            'attribute': ['id', 'name', 'administrative_region', 'country'],
        }
