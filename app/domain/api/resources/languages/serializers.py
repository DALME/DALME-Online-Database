"""Serializers for language data."""

from domain.api.serializers import DynamicSerializer
from domain.models import LanguageReference


class LanguageReferenceSerializer(DynamicSerializer):
    """Serializer for languages."""

    class Meta:
        model = LanguageReference
        fields = [
            'id',
            'glottocode',
            'iso6393',
            'name',
            'is_dialect',
            'parent',
        ]
        field_sets = {
            'option': [
                'id',
                'name',
            ],
            'attribute': [
                'id',
                'name',
                'iso6393',
            ],
        }
