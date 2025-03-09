"""Serializers for comment data."""

from domain.api.resources.tenants import TenantSerializer
from domain.api.resources.users import UserSerializer
from domain.api.serializers import DynamicSerializer
from domain.models import Comment


class CommentSerializer(DynamicSerializer):
    """Serializer for comments."""

    creation_user = UserSerializer(field_set='attribute', required=False)
    tenant = TenantSerializer(required=True)

    class Meta:
        model = Comment
        fields = [
            'tenant',
            'body',
            'creation_timestamp',
            'creation_user',
        ]
