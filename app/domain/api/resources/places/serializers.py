"""Serializers for place data."""

from rest_framework import serializers

from domain.api.resources.tags import TagSerializer
from domain.api.serializers import DynamicSerializer
from domain.models import Place


class PlaceSerializer(DynamicSerializer):
    """Serializer for places."""

    attribute_ids = serializers.PrimaryKeyRelatedField(source='attributes', required=False, read_only=True, many=True)
    creation_user_id = serializers.PrimaryKeyRelatedField(source='creation_user', required=False, read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(source='location', required=False, read_only=True)
    modification_user_id = serializers.PrimaryKeyRelatedField(
        source='modification_user', required=False, read_only=True
    )
    object_id = serializers.SerializerMethodField()
    record_attestation_count = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Place
        fields = [
            'attestation_count',
            'attribute_ids',
            'comment_count',
            'creation_timestamp',
            'creation_user_id',
            'id',
            'location_id',
            'modification_timestamp',
            'modification_user_id',
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
