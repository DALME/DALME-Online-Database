from dalme_app.models import Workflow
from rest_framework import serializers
from dalme_app.utils import round_timesince
import datetime
from dalme_api.serializers.users import UserSerializer


class WorkflowSerializer(serializers.ModelSerializer):
    """Basic serializer for workflow control"""
    last_user = UserSerializer(fields=['username', 'profile'], required=False)

    class Meta:
        model = Workflow
        fields = ('help_flag', 'is_public', 'last_modified', 'last_user', 'wf_status', 'stage', 'status',
                  'ingestion_done', 'transcription_done', 'markup_done', 'parsing_done', 'review_done')
        extra_kwargs = {'last_user': {'required': False}, }

