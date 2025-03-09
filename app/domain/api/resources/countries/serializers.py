"""Serializers for country data."""

from domain.api.serializers import DynamicSerializer
from domain.models import CountryReference


class CountryReferenceSerializer(DynamicSerializer):
    """Serializer for countries."""

    class Meta:
        model = CountryReference
        fields = [
            'id',
            'name',
            'alpha_2_code',
            'alpha_3_code',
            'num_code',
        ]
        field_sets = {
            'option': [
                'id',
                'name',
            ],
            'attribute': [
                'id',
                'name',
            ],
        }
