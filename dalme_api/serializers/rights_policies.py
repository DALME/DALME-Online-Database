"""Serializers for rights policies."""
from rest_framework import serializers

from dalme_api.serializers.others import AttachmentSerializer
from dalme_api.serializers.users import UserSerializer
from dalme_app.models import RightsPolicy


class RightsPolicySerializer(serializers.ModelSerializer):
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
        extra_kwargs = {
            'rights_notice': {'required': False},
            'licence': {'required': False},
            'attachments': {'required': False},
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['rights_status'] = {
            'name': instance.get_rights_status_display(),
            'id': ret.pop('rights_status'),
        }
        return ret

    def to_internal_value(self, data):
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

    @staticmethod
    def get_comment_count(obj):
        return obj.comments.count()
