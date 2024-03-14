"""Serializers for comment data."""

from rest_framework import serializers

from api.resources.tenants import TenantSerializer
from api.resources.users import UserSerializer
from ida.models import Comment


class CommentSerializer(serializers.ModelSerializer):
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
