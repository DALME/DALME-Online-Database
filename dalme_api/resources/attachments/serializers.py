"""Serializers for attachment data."""
from rest_framework import serializers

from dalme_app.models import Attachment


class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for attachments."""

    class Meta:
        model = Attachment
        fields = ('filename', 'source', 'filetype')
