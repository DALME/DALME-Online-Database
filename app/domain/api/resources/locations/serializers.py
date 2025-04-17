"""Serializers for location data."""

from rest_framework import serializers

from domain.api.resources.attributes import AttributeSerializer
from domain.api.resources.tags import TagSerializer
from domain.api.resources.users import UserSerializer
from domain.api.serializers import DynamicSerializer
from domain.models import Location


class LocationSerializer(DynamicSerializer):
    """Serializer for places."""

    attributes = AttributeSerializer(many=True, required=False)
    location_type = serializers.CharField(source='get_location_type_display')
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
