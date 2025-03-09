"""Serializers for place data."""

from domain.api.resources.attributes import AttributeSerializer
from domain.api.resources.locations import LocationSerializer
from domain.api.resources.tags import TagSerializer
from domain.api.serializers import DynamicSerializer
from domain.models import Place


class PlaceSerializer(DynamicSerializer):
    """Serializer for places."""

    attributes = AttributeSerializer(many=True, required=False)
    location = LocationSerializer(field_set='attribute')
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Place
        fields = [
            'id',
            'name',
            'attributes',
            'location',
            'comment_count',
            'tags',
        ]
        field_sets = {
            'option': [
                'id',
                'name',
            ],
            'attribute': [
                'id',
                'name',
                'location',
            ],
        }
