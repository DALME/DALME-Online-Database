"""Serializers for comment data."""
from rest_framework import serializers

from dalme_api.serializers.users import UserSerializer
from dalme_app.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments."""

    creation_user = UserSerializer(field_set='attribute', required=False)

    class Meta:
        model = Comment
        fields = ('body', 'creation_timestamp', 'creation_user')
