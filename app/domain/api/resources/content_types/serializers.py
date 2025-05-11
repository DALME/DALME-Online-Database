"""Serializers for content type data."""

from rest_framework import serializers

from django.contrib.contenttypes.models import ContentType

from domain.api.serializers import DynamicSerializer
from domain.models import ContentAttributes, ContentTypeExtended


class ContentTypeSerializer(DynamicSerializer):
    """Serializer for base Django content types."""

    class Meta:
        model = ContentType
        fields = [
            'id',
            'app_label',
            'model',
        ]


class ContentAttributesSerializer(DynamicSerializer):
    """Serializer for content attributes bound to an extended content type."""

    id = serializers.ReadOnlyField(source='attribute_type.id')
    name = serializers.ReadOnlyField(source='attribute_type.name')
    label = serializers.ReadOnlyField(source='attribute_type.label')
    description = serializers.ReadOnlyField(source='attribute_type.description')
    data_type = serializers.ReadOnlyField(source='attribute_type.data_type')
    is_local = serializers.ReadOnlyField(source='attribute_type.is_local')

    class Meta:
        model = ContentAttributes
        fields = [
            'id',
            'name',
            'label',
            'description',
            'data_type',
            'is_local',
            'is_required',
            'is_unique',
            'override_label',
            'override_description',
        ]


class ExtendedContentTypeSerializer(DynamicSerializer):
    """Serializer for extended content types."""

    attribute_types = ContentAttributesSerializer(source='attributes_list', many=True, required=False)

    class Meta:
        model = ContentTypeExtended
        fields = [
            'id',
            'name',
            'description',
            'is_abstract',
            'attribute_types',
            'parent',
            'can_view',
            'can_edit',
            'can_delete',
            'can_add',
            'can_remove',
        ]
        field_sets = {
            'attribute': [
                'id',
                'name',
                'short_name',
                'is_abstract',
                'description',
            ],
        }
        extra_kwargs = {
            'name': {
                'validators': [],
            },
        }
