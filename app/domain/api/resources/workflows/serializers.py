"""Serializers for workflow data."""

from rest_framework import serializers

from domain.models import Workflow, WorkLog


class WorklogSerializer(serializers.ModelSerializer):
    """Basic serializer for work logs."""

    user_id = serializers.PrimaryKeyRelatedField(source='user', required=False, read_only=True)

    class Meta:
        model = WorkLog
        fields = [
            'id',
            'event',
            'record',
            'timestamp',
            'user_id',
        ]


class WorkflowSerializer(serializers.ModelSerializer):
    """Basic serializer for workflow control."""

    last_user_id = serializers.PrimaryKeyRelatedField(source='last_user', required=False, read_only=True)
    work_log = WorklogSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Workflow
        fields = [
            'help_flag',
            'ingestion_done',
            'is_public',
            'last_modified',
            'last_user_id',
            'markup_done',
            'parsing_done',
            'record',
            'review_done',
            'stage',
            'status',
            'transcription_done',
            'wf_status',
            'work_log',
        ]
        extra_kwargs = {
            'last_user': {
                'required': False,
            }
        }
