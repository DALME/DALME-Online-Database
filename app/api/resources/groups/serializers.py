"""Serializers for group data."""

from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from django.contrib.auth.models import Group

from api.dynamic_serializer import DynamicSerializer
from api.resources.tenants import TenantSerializer
from oauth.models import GroupProperties


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
    tenant = TenantSerializer(allow_null=True, source='properties.tenant')

    class Meta:
        model = Group
        fields = [
            'id',
            'tenant',
            'name',
            'group_type',
            'description',
        ]
        field_sets = {
            'option': [
                'id',
                'name',
                'group_type',
                'description',
                'tenant',
            ],
            'attribute': [
                'id',
                'name',
                'group_type',
                'description',
                'tenant',
            ],
        }
        extra_kwargs = {
            'name': {
                'required': False,
            },
        }
