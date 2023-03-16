"""Serializers for place data."""
from dalme_api.serializers.tags import TagSerializer
from dalme_app.models import Place

from .attributes import AttributeSerializer
from .base_classes import DynamicSerializer
from .locations import LocationSerializer


class PlaceSerializer(DynamicSerializer):
    """Serializer for places."""

    attributes = AttributeSerializer(many=True, required=False)
    location = LocationSerializer(field_set='attribute')
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Place
        fields = ('id', 'name', 'attributes', 'location', 'comment_count', 'tags')
        field_sets = {
            'option': ['id', 'name'],
            'attribute': ['id', 'name', 'location'],
        }
