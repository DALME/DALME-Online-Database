from dalme_api.serializers.tags import TagSerializer
from dalme_app.models import Location

from .attributes import AttributeSerializer
from .base_classes import DynamicSerializer
from .users import UserSerializer


class LocationSerializer(DynamicSerializer):
    """Serializer for places."""

    attributes = AttributeSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)
    creation_user = UserSerializer(field_set='attribute')
    modification_user = UserSerializer(field_set='attribute')

    class Meta:  # noqa: D106
        model = Location
        fields = (
            'id',
            'location_type',
            'attributes',
            'comment_count',
            'tags',
            'creation_timestamp',
            'creation_user',
            'modification_timestamp',
            'modification_user',
        )
        field_sets = {
            'option': ['id', 'location_type', 'attributes'],
            'attribute': ['id', 'location_type', 'attributes'],
        }
