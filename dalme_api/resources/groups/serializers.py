"""Serializers for group data."""
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from django.contrib.auth.models import Group

from dalme_api.dynamic_serializer import DynamicSerializer
from ida.models import GroupProperties


class GroupSerializer(DynamicSerializer, WritableNestedModelSerializer):
    """Serializer for user group data."""

    group_type = serializers.ChoiceField(
        choices=GroupProperties.GROUP_TYPES,
        source='properties.get_group_type_display',
        required=False,
    )
    description = serializers.CharField(
        max_length=255,
        source='properties.description',
        required=False,
    )
    tenant = serializers.PrimaryKeyRelatedField(
        allow_null=True,
        many=False,
        read_only=True,
        source='properties.tenant',
    )

    class Meta:
        model = Group
        fields = ('id', 'name', 'group_type', 'description', 'tenant')
        field_sets = {
            'option': ['id', 'name', 'group_type', 'description', 'tenant'],
            'attribute': ['id', 'name', 'group_type', 'description', 'tenant'],
        }
        extra_kwargs = {'name': {'required': False}}
