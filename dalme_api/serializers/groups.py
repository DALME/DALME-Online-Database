"""Serializers for group data."""
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from django.contrib.auth.models import Group

from dalme_app.models import GroupProperties

from .base_classes import DynamicSerializer


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

    class Meta:
        model = Group
        fields = ('id', 'name', 'group_type', 'description')
        field_sets = {
            'option': ['id', 'name', 'group_type', 'description'],
            'attribute': ['id', 'name', 'group_type', 'description'],
        }
        extra_kwargs = {'name': {'required': False}}
