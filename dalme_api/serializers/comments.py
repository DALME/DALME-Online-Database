from dalme_app.models import Comment
from rest_framework import serializers
from dalme_api.serializers.users import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    creation_user = UserSerializer(fields=['full_name', 'username', 'id', 'avatar'])

    class Meta:
        model = Comment
        fields = ('body', 'creation_timestamp', 'creation_user')
