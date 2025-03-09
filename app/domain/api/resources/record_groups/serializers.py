"""Serializers for record group data."""

from rest_framework import serializers

from domain.api.resources.agents import AgentSerializer
from domain.api.resources.attributes import AttributeSerializer

# from domain.api.resources.locales import LocaleReferenceSerializer
from domain.api.resources.records import RecordSerializer
from domain.api.resources.users import UserSerializer
from domain.api.serializers import BaseContentTypeSerializer, DynamicSerializer
from domain.models import RecordGroup


class RecordGroupSerializer(DynamicSerializer):
    """Serializer for record groups."""

    attributes = AttributeSerializer(many=True, required=False)
    children = RecordSerializer(field_set='attribute', many=True, required=False)
    owner = UserSerializer(field_set='attribute', required=False)
    parent = AgentSerializer(required=False)
    parent_type = BaseContentTypeSerializer(required=False)
    creation_user = UserSerializer(field_set='attribute', required=False)
    modification_user = UserSerializer(field_set='attribute', required=False)
    # annotated fields
    description = serializers.ReadOnlyField()
    type = serializers.ReadOnlyField()
    mk1_identifier = serializers.ReadOnlyField()
    authority = serializers.ReadOnlyField()
    format = serializers.ReadOnlyField()
    support = serializers.ReadOnlyField()
    # locale = LocaleReferenceSerializer()
    archival_series = serializers.ReadOnlyField()
    archival_number = serializers.ReadOnlyField()

    class Meta:
        model = RecordGroup
        fields = [
            'id',
            'name',
            'short_name',
            'owner',
            'parent',
            'parent_type',
            'children',
            'attributes',
            'is_private',
            'no_records',
            'comment_count',
            'creation_timestamp',
            'creation_user',
            'modification_timestamp',
            'modification_user',
            'description',
            'type',
            'mk1_identifier',
            'authority',
            'format',
            'support',
            # 'locale',
            'archival_series',
            'archival_number',
        ]
        default_exclude = [
            # 'parent',
            # 'parent_type',
            # 'children',
            # 'attributes',
        ]
        field_sets = {
            'attribute': [
                'id',
                'name',
                'short_name',
            ],
            'collection_member': [
                'id',
                'name',
            ],
            'option': [
                'id',
                'name',
            ],
            'parent': [
                'id',
                'name',
                'short_name',
                'owner',
                'parent',
                'parent_type',
                'attributes',
                'is_private',
                'no_records',
                'comment_count',
                'creation_timestamp',
                'creation_user',
                'modification_timestamp',
                'modification_user',
            ],
        }
