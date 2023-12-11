"""Serializers for locale data."""
from dalme_api.dynamic_serializer import DynamicSerializer
from dalme_api.resources.countries import CountryReferenceSerializer
from dalme_app.models import LocaleReference


class LocaleReferenceSerializer(DynamicSerializer):
    """Serializer for locales."""

    country = CountryReferenceSerializer(field_set='attribute')

    class Meta:
        model = LocaleReference
        fields = ('id', 'name', 'administrative_region', 'country', 'latitude', 'longitude')
        field_sets = {
            'option': ['id', 'name', 'country'],
            'attribute': ['id', 'name', 'administrative_region', 'country'],
        }
