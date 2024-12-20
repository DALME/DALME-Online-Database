"""Serializers for tag data."""

from rest_framework import serializers

from api.resources.tenants import TenantSerializer
from domain.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag data."""

    tag_type_name = serializers.ChoiceField(
        choices=Tag.TAG_TYPES,
        source='get_tag_type_display',
        required=False,
    )
    tenant = TenantSerializer(required=True)

    class Meta:
        model = Tag
        fields = [
            'tag',
            'tag_group',
            'tag_type',
            'tag_type_name',
            'tenant',
        ]
        extra_kwargs = {
            'tag_type': {
                'required': False,
            },
        }
