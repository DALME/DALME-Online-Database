import textwrap

from rest_framework import serializers

from django.conf import settings
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

        if settings.IS_V2:
            ret['group'] = {"id": group.id, "name": group.name}
        else:
            ret['group'] = group.name

        if 'task_count' in ret:
            task_count = ret['task_count']
        else:
            task_count = 0
        ret['name'] = '<div class="d-flex"><div class="align-self-start mr-auto">'+ret['name']+'</div>\
                       <div class="badge badge-primary badge-pill align-self-end">'+str(task_count)+'</div></div>'
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

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['comment_count'] = instance.comments.count()
        task = '<div class="d-flex align-items-center mb-1"><a href="/tasks/{}" class="task-title">{}</a>'.format(ret['id'], ret['title'])
        if ret['comment_count'] > 0:
            task += '<div class="align-self-end ml-auto d-flex mr-2 align-items-center"><i class="fas fa-comment fa-lg icon-badge">\
            </i><span class="icon-badge-count">{}</span></div>'.format(ret['comment_count'])
        task += '</div><div class="task-description">{}</div>'.format(ret['description'])
        ret['task'] = task
        attachments = ''
        attachments_detail = ''
        if ret['workset'] is not None:
            attachments += '<a href="/sets/{}" class="task-attachment">Workset</a>'.format(ret['workset'])
            attachments_detail += '<a href="/sets/{}" class="task-attachment">Workset: {}</a>'.format(ret['workset'], instance.workset.name)
        if ret['url'] is not None:
            attachments += '<a href="{}" class="task-attachment">URL</a>'.format(ret['url'])
            attachments_detail += '<a href="{}" class="task-attachment">URL: {}</a>'.format(ret['url'], textwrap.shorten(instance.url, width=35, placeholder="..."))
        if ret['file'] is not None:
            attachments += '<a href="/download/{}" class="task-attachment">File</a>'.format(instance.file.file)
            attachments_detail += '<a href="/download/{}" class="task-attachment">File: {}</a>'.format(instance.file.file, instance.file.filename)
        ret['attachments'] = attachments
        ret['attachments_detail'] = attachments_detail
        overdue = ret.pop('overdue_status')
        dates = '<div class="task-date">Cre: ' + ret['creation_timestamp'] + '</div>'
        dates_detail = '<span class="task-date">Created: ' + ret['creation_timestamp'] + ' by '+instance.creation_user.username+'</span>'
        if ret['due_date'] is not None:
            dates += '<div class="task-date task-'
            dates_detail += '<span class="task-date task-'
            if overdue:
                dates += 'over'
                dates_detail += 'over'
            dates += 'due">Due: ' + ret['due_date'] + '</div>'
            dates_detail += 'due">Due: ' + ret['due_date'] + '</span>'
        if ret['completed_date'] is not None:
            dates += '<div class="task-date task-completed">Com: ' + ret['completed_date'] + '</div>'
            dates_detail += '<span class="task-date task-completed">Completed: ' + ret['completed_date'] + '</span>'
        ret['dates'] = dates
        ret['dates_detail'] = dates_detail
        if ret['assigned_to'] is None:
            ret['assigned_to'] = instance.task_list.group.name
        else:
            ret['assigned_to'] = instance.assigned_to.profile.full_name

        # TODO: No need for handling if we fix profile create via createsuperuser.
        try:
            ret['owner'] = instance.creation_user.profile.full_name
        except Profile.RelatedObjectDoesNotExist:
            ret['owner'] = instance.creation_user.username

        return ret
