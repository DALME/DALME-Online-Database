"""Serializers for publication data."""

from domain.api.resources.attributes import AttributeSerializer
from domain.api.resources.records import RecordSerializer
from domain.api.resources.users import UserSerializer
from domain.api.serializers import DynamicSerializer
from domain.models import Publication


class PublicationSerializer(DynamicSerializer):
    """Serializer for publications."""

    attributes = AttributeSerializer(many=True, required=False)
    children = RecordSerializer(field_set='attribute', many=True, required=False)
    creation_user = UserSerializer(field_set='attribute', required=False)
    modification_user = UserSerializer(field_set='attribute', required=False)

    class Meta:
        model = Publication
        fields = [
            'id',
            'name',
            'short_name',
            'attributes',
            'children',
            'comment_count',
            'creation_timestamp',
            'creation_user',
            'modification_timestamp',
            'modification_user',
        ]
        field_sets = {
            'attribute': [
                'id',
                'name',
                'short_name',
            ],
            'option': [
                'id',
                'name',
            ],
            'parent': [
                'id',
                'name',
                'short_name',
                'attributes',
                'comment_count',
                'creation_timestamp',
                'creation_user',
                'modification_timestamp',
                'modification_user',
            ],
        }
