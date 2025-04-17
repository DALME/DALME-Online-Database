"""Serializers for locale data."""

from domain.api.resources.countries import CountryReferenceSerializer
from domain.api.serializers import DynamicSerializer
from domain.models import LocaleReference


class LocaleReferenceSerializer(DynamicSerializer):
    """Serializer for locales."""

    country = CountryReferenceSerializer(field_set='attribute')

    class Meta:
        model = LocaleReference
        fields = [
            'id',
            'name',
            'administrative_region',
            'country',
            'latitude',
            'longitude',
        ]
        field_sets = {
            'option': [
                'id',
                'name',
                'country',
            ],
            'attribute': [
                'id',
                'name',
                'administrative_region',
                'country',
                'latitude',
                'longitude',
            ],
        }
