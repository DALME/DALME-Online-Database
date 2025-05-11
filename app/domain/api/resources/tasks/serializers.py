"""Serializers for task data."""

from rest_framework import serializers

from domain.api.resources.attachments import AttachmentSerializer
from domain.api.resources.collections import CollectionSerializer
from domain.api.resources.tenants import TenantSerializer
from domain.api.serializers import DynamicSerializer
from domain.models import Task, TaskList


class TaskListSerializer(DynamicSerializer):
    """Serializer for task lists."""

    creation_user_id = serializers.PrimaryKeyRelatedField(source='creation_user', required=False, read_only=True)
    modification_user_id = serializers.PrimaryKeyRelatedField(
        source='modification_user', required=False, read_only=True
    )
    owner_id = serializers.PrimaryKeyRelatedField(source='owner', required=False, read_only=True)
    team_link_id = serializers.PrimaryKeyRelatedField(source='team_link', required=False, read_only=True)
    tenant = TenantSerializer(required=True)

    class Meta:
        model = TaskList
        fields = [
            'creation_timestamp',
            'creation_user_id',
            'description',
            'id',
            'modification_timestamp',
            'modification_user_id',
            'name',
            'owner_id',
            'slug',
            'task_count',
            'team_link_id',
            'tenant',
        ]


class TaskSerializer(DynamicSerializer):
    """Serializer for tasks."""

    assignee_ids = serializers.PrimaryKeyRelatedField(source='assignees', required=False, read_only=True, many=True)
    completed_by_id = serializers.PrimaryKeyRelatedField(source='completed_by', required=False, read_only=True)
    creation_user_id = serializers.PrimaryKeyRelatedField(source='creation_user', required=False, read_only=True)
    files = AttachmentSerializer(many=True, required=False)
    modification_user_id = serializers.PrimaryKeyRelatedField(
        source='modification_user', required=False, read_only=True
    )
    resources = CollectionSerializer(many=True, field_set='attribute', required=False)
    task_list_id = serializers.PrimaryKeyRelatedField(source='task_list', required=False, read_only=True)
    tenant = TenantSerializer(required=True)

    class Meta:
        model = Task
        fields = [
            'assignee_ids',
            'comment_count',
            'completed_by_id',
            'completed_date',
            'completed',
            'creation_timestamp',
            'creation_user_id',
            'description',
            'due_date',
            'files',
            'id',
            'modification_timestamp',
            'modification_user_id',
            'overdue',
            'resources',
            'task_list_id',
            'tenant',
            'title',
            'url',
        ]
        extra_kwargs = {
            'overdue': {
                'required': False,
            },
            'comment_count': {
                'required': False,
            },
        }
