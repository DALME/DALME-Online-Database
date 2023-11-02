"""Serializers for rights data."""
from rest_framework import serializers

from dalme_app.models import RightsPolicy

from .attachments import AttachmentSerializer
from .base_classes import DynamicSerializer
from .users import UserSerializer


class RightsPolicySerializer(DynamicSerializer):
    """Serializer for rights policies."""

    attachments = AttachmentSerializer(required=False)
    comment_count = serializers.SerializerMethodField(required=False)
    creation_user = UserSerializer(fields=['full_name', 'username', 'id', 'avatar'], required=False)
    modification_user = UserSerializer(fields=['full_name', 'username', 'id', 'avatar'], required=False)

    class Meta:
        model = RightsPolicy
        fields = (
            'id',
            'name',
            'rights_holder',
            'rights_status',
            'rights',
            'public_display',
            'notice_display',
            'rights_notice',
            'licence',
            'attachments',
            'creation_timestamp',
            'creation_user',
            'modification_user',
            'modification_timestamp',
            'comment_count',
        )
        field_sets = {
            'attribute': [
                'id',
                'name',
                'rights_holder',
                'rights_status',
                'rights',
                'public_display',
                'notice_display',
                'rights_notice',
            ],
        }
        extra_kwargs = {
            'rights_notice': {'required': False},
            'licence': {'required': False},
            'attachments': {'required': False},
        }

    def get_comment_count(self, obj):
        """Return count of comments."""
        return obj.comments.count()

    def to_representation(self, instance):
        """Transform outgoing data."""
        ret = super().to_representation(instance)
        ret['rights_status'] = {
            'name': instance.get_rights_status_display(),
            'id': ret.pop('rights_status'),
        }
        return ret

    def to_internal_value(self, data):
        """Transform incoming data."""
        if data.get('attachments') is not None:
            if data['attachments'].get('file') is not None:
                if (
                    isinstance(data['attachments']['file'], dict)
                    and data['attachments']['file'].get('file_id') is not None
                ):
                    data['attachments'] = data['attachments']['file']['file_id']
                else:
                    data['attachments'] = data['attachments']['file']
            else:
                data.pop('attachments')

        if data.get('rights_status') is not None and data['rights_status'].get('id') is not None:
            data['rights_status'] = data['rights_status']['id']

        return super().to_internal_value(data)
