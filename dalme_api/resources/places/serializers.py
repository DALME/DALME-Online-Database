"""Serializers for place data."""
from dalme_api.dynamic_serializer import DynamicSerializer
from dalme_api.resources.attributes import AttributeSerializer
from dalme_api.resources.locations import LocationSerializer
from dalme_api.resources.tags import TagSerializer
from ida.models import Place


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
