from dalme_app.models import ContentAttributes, ContentTypeExtended

from .attribute_types import AttributeTypeSerializer
from .base_classes import DynamicSerializer


class ContentTypeSerializer(DynamicSerializer):
    """Serializer for content types."""

    attribute_types = AttributeTypeSerializer(many=True, required=False)

    class Meta:  # noqa: D106
        model = ContentTypeExtended
        fields = (
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
        )
        field_sets = {
            'attribute': ['id', 'name', 'short_name', 'is_abstract', 'description'],
        }
        extra_kwargs = {'name': {'validators': []}}


class ContentAttributesSerializer(DynamicSerializer):
    """Serializer for content attributes."""

    content_type = ContentTypeSerializer(required=False)
    attribute_type = AttributeTypeSerializer(required=False)

    class Meta:  # noqa: D106
        model = ContentAttributes
        fields = (
            'id',
            'content_type',
            'attribute_type',
            'order',
            'required',
            'unique',
        )
