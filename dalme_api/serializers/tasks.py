import textwrap
from rest_framework import serializers
from django.contrib.auth.models import Group
from dalme_api.serializers.users import UserSerializer
from dalme_app.models import Profile, Task, TaskList


class TaskListSerializer(serializers.ModelSerializer):
    task_count = serializers.IntegerField(required=False)

    class Meta:
        model = TaskList
        fields = ('id', 'name', 'group', 'task_count')

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        group = Group.objects.get(pk=ret['group'])
        task_list_groups = group.task_list_group.all()
        for task_list_group in task_list_groups:
            tasks = task_list_group.task_set.all()
            task_ids = [task.pk for task in tasks]
            if task_list_group.name == ret['name']:
                ret['task_index'] = task_ids
        return ret


class TaskSerializer(serializers.ModelSerializer):
    creation_timestamp = serializers.DateTimeField(format='%d-%b-%Y', required=False)
    completed_date = serializers.DateTimeField(format='%d-%b-%Y', required=False, allow_null=True)
    due_date = serializers.DateField(format='%d-%b-%Y', required=False, allow_null=True)
    creation_user = UserSerializer(fields=['full_name', 'username', 'id', 'avatar'], required=False)
    task_list = TaskListSerializer(required=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'task_list', 'due_date', 'completed', 'completed_date', 'created_by', 'assigned_to', 'description',
                  'workset', 'url', 'creation_timestamp', 'overdue_status', 'file', 'creation_user',)


        return ret
