"""Serializers for location data."""

from api.dynamic_serializer import DynamicSerializer
from api.resources.attributes import AttributeSerializer
from api.resources.tags import TagSerializer
from api.resources.users import UserSerializer
from domain.models import Location


class LocationSerializer(DynamicSerializer):
    """Serializer for places."""

    attributes = AttributeSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)
    creation_user = UserSerializer(field_set='attribute')
    modification_user = UserSerializer(field_set='attribute')

    class Meta:
        model = Location
        fields = [
            'id',
            'location_type',
            'attributes',
            'comment_count',
            'tags',
            'creation_timestamp',
            'creation_user',
            'modification_timestamp',
            'modification_user',
        ]
        field_sets = {
            'option': [
                'id',
                'location_type',
                'attributes',
            ],
            'attribute': [
                'id',
                'location_type',
                'attributes',
            ],
        }
