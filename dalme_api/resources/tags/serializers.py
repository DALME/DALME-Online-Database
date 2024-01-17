"""Serializers for tag data."""
from rest_framework import serializers

from dalme_app.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag data."""

    tag_type_name = serializers.ChoiceField(
        choices=Tag.TAG_TYPES,
        source='get_tag_type_display',
        required=False,
    )

    class Meta:
        model = Tag
        fields = [
            'tag_type',
            'tag',
            'tag_group',
            'tag_type_name',
        ]
        extra_kwargs = {
            'tag_type': {
                'required': False,
            },
        }
