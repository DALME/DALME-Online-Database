from dalme_app.models import Workflow
from rest_framework import serializers
from dalme_app.utils import round_timesince
import datetime
from dalme_app.serializers.users import UserSerializer


class WorkflowSerializer(serializers.ModelSerializer):
    """Basic serializer for workflow control"""
    last_user = UserSerializer(fields=['username', 'profile'], required=False)

    class Meta:
        model = Workflow
        fields = ('help_flag', 'is_public', 'last_modified', 'last_user', 'wf_status', 'stage', 'status',
                  'ingestion_done', 'transcription_done', 'markup_done', 'parsing_done', 'review_done')
        extra_kwargs = {'last_user': {'required': False}, }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        tstamp = ret.pop('last_modified')
        last_user = ret.pop('last_user')
        ret['activity'] = {
            # version of code that needs Python 3.7 to work
            # 'timestamp': round_timesince(datetime.datetime.fromisoformat(ret.pop('last_modified'))),
            # version for Python 3.6 (has to remove : from utcoffset because ISO standard is not properly implemented)
            'timestamp': round_timesince(datetime.datetime.strptime(tstamp[0:-3:]+tstamp[-2::], '%Y-%m-%dT%H:%M:%S.%f%z')),
            'user': last_user['profile']['full_name'],
            'username': last_user['username']
        }
        return ret
