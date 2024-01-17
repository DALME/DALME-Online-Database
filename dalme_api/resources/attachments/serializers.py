"""Serializers for attachment data."""
from rest_framework import serializers

from dalme_api.resources.tenants import TenantSerializer
from dalme_app.models import Attachment


class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for attachments."""

    tenant = TenantSerializer(required=True)

    class Meta:
        model = Attachment
        fields = [
            'tenant',
            'filename',
            'source',
            'filetype',
        ]
