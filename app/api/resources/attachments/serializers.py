"""Serializers for attachment data."""

from rest_framework import serializers

from api.resources.tenants import TenantSerializer
from domain.models import Attachment


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
