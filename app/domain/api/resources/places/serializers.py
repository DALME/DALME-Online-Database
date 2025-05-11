"""Serializers for place data."""

from rest_framework import serializers

from domain.api.resources.attributes import AttributeSerializer
from domain.api.resources.locations import LocationSerializer
from domain.api.resources.tags import TagSerializer
from domain.api.resources.users import UserSerializer
from domain.api.serializers import DynamicSerializer
from domain.models import Place


class PlaceSerializer(DynamicSerializer):
    """Serializer for places."""

    attributes = AttributeSerializer(many=True, required=False)
    creation_user = UserSerializer(field_set='attribute', required=False)
    location = LocationSerializer(field_set='attribute')
    modification_user = UserSerializer(field_set='attribute', required=False)
    object_id = serializers.SerializerMethodField()
    record_attestation_count = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Place
        fields = [
            'attestation_count',
            'attributes',
            'comment_count',
            'creation_timestamp',
            'creation_user',
            'id',
            'location',
            'modification_timestamp',
            'modification_user',
            'name',
            'object_id',
            'record_attestation_count',
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

    def get_record_attestation_count(self, obj):
        """Return count of attestations for current record."""
        if self.context.get('record'):
            return obj.get_attestations_for_record(self.context['record'])
        return None

    def get_object_id(self, _):
        """Return id for current record."""
        if self.context.get('record'):
            return self.context['record'].id
        return None
