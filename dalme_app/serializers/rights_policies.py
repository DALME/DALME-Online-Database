from dalme_app.models import RightsPolicy
from rest_framework import serializers


class RightsPolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = RightsPolicy
        fields = ('id', 'name', 'rights_holder', 'rights_status', 'rights', 'notice_display', 'rights_notice', 'licence', 'attachments')
        extra_kwargs = {
                        'rights_notice': {'required': False},
                        'licence': {'required': False},
                        'attachments': {'required': False}
                        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret['attachments'] is not None:
            a_pill = '<a href="/download/{}" class="task-attachment">File</a>'.format(instance.attachments.file)
            ret['attachments'] = {
                'pill': a_pill,
                'file': {
                    'file_id': ret.pop('attachments'),
                    'filename': instance.attachments.filename
                }
            }
        ret['rights_status'] = {
            'name': instance.get_rights_status_display,
            'value': ret.pop('rights_status')
        }
        return ret
