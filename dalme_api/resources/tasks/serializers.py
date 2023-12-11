"""Serializers for task data."""
from rest_framework import serializers

from dalme_api.resources.attachments import AttachmentSerializer
from dalme_api.resources.collections import CollectionSerializer
from dalme_api.resources.groups import GroupSerializer
from dalme_api.resources.users import UserSerializer
from dalme_app.models import Task, TaskList


class TaskListSerializer(serializers.ModelSerializer):
    """Serializer for task lists."""

    team_link = GroupSerializer(field_set='attribute', required=False)
    owner = UserSerializer(field_set='attribute')
    creation_user = UserSerializer(field_set='attribute', required=False)
    modification_user = UserSerializer(field_set='attribute', required=False)

    class Meta:
        model = TaskList
        fields = (
            'id',
            'name',
            'description',
            'slug',
            'team_link',
            'owner',
            'task_count',
            'creation_user',
            'creation_timestamp',
            'modification_user',
            'modification_timestamp',
        )


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for tasks."""

    task_list = TaskListSerializer(required=True)
    completed_by = UserSerializer(field_set='attribute', required=False)
    files = AttachmentSerializer(many=True, required=False)
    assignees = UserSerializer(many=True, field_set='attribute', required=False)
    resources = CollectionSerializer(many=True, field_set='attribute', required=False)
    creation_user = UserSerializer(field_set='attribute', required=False)
    modification_user = UserSerializer(field_set='attribute', required=False)

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'task_list',
            'description',
            'due_date',
            'completed',
            'completed_date',
            'completed_by',
            'overdue',
            'files',
            'resources',
            'assignees',
            'url',
            'comment_count',
            'creation_timestamp',
            'creation_user',
            'modification_user',
            'modification_timestamp',
        )
        extra_kwargs = {
            'overdue': {'required': False},
            'comment_count': {'required': False},
        }
