from rest_framework import serializers
from dalme_api.serializers.users import UserSerializer
from dalme_app.models import Task, TaskList
from dalme_api.serializers.others import GroupSerializer
from dalme_api.serializers.others import AttachmentSerializer


class TaskListSerializer(serializers.ModelSerializer):
    task_count = serializers.IntegerField(required=False)
    group = GroupSerializer(required=False)

    class Meta:
        model = TaskList
        fields = ('id', 'name', 'group', 'task_count')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        group = instance.group
        task_list_groups = group.task_list_group.all()
        for task_list_group in task_list_groups:
            tasks = task_list_group.task_set.all()
            task_ids = [task.pk for task in tasks]
            if task_list_group.name == ret['name']:
                ret['task_index'] = task_ids
        return ret


class TaskSerializer(serializers.ModelSerializer):
    creation_user = UserSerializer(fields=['full_name', 'username', 'id', 'avatar'], required=False)
    modification_user = UserSerializer(fields=['full_name', 'username', 'id', 'avatar'], required=False)
    task_list = TaskListSerializer(required=True)
    assigned_to = UserSerializer(fields=['full_name', 'username', 'id', 'avatar'], required=False)
    comment_count = serializers.SerializerMethodField(required=False)
    file = AttachmentSerializer(required=False)

    class Meta:
        model = Task
        fields = ('id', 'title', 'task_list', 'due_date', 'completed', 'completed_date',
                  'assigned_to', 'description', 'workset', 'url', 'creation_timestamp',
                  'overdue_status', 'file', 'creation_user', 'comment_count',
                  'modification_user', 'modification_timestamp')

    def get_comment_count(self, obj):
        return obj.comments.count()
