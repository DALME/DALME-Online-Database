"""Serializers for comment data."""
from rest_framework import serializers

from dalme_api.resources.tenants import TenantSerializer
from dalme_api.resources.users import UserSerializer
from dalme_app.models import Comment


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
