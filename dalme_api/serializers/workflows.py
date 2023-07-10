from rest_framework import serializers

from dalme_api.serializers.users import UserSerializer
from dalme_app.models import Workflow, WorkLog


class WorklogSerializer(serializers.ModelSerializer):
    """Basic serializer for work logs."""

    user = UserSerializer(field_set='attribute', required=False)

    class Meta:  # noqa: D106
        model = WorkLog
        fields = ('id', 'event', 'timestamp', 'user')


class WorkflowSerializer(serializers.ModelSerializer):
    """Basic serializer for workflow control."""

    last_user = UserSerializer(field_set='attribute', required=False)
    work_log = WorklogSerializer(many=True, read_only=True, required=False)

    class Meta:  # noqa: D106
        model = Workflow
        fields = (
            'help_flag',
            'is_public',
            'last_modified',
            'last_user',
            'wf_status',
            'stage',
            'status',
            'ingestion_done',
            'transcription_done',
            'markup_done',
            'parsing_done',
            'review_done',
            'work_log',
        )
        extra_kwargs = {'last_user': {'required': False}}
