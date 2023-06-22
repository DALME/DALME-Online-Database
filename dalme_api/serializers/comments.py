from rest_framework import serializers

from dalme_api.serializers.users import UserSerializer
from dalme_app.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments."""

    creation_user = UserSerializer(field_set='attribute')

    class Meta:  # noqa: D106
        model = Comment
        fields = ('body', 'creation_timestamp', 'creation_user')
