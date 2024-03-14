"""Serializers for language data."""

from api.dynamic_serializer import DynamicSerializer
from ida.models import LanguageReference


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
