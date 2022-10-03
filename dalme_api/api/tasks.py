from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from dalme_api.serializers import TaskSerializer, TaskListSerializer
from dalme_api.access_policies import TaskAccessPolicy, TaskListAccessPolicy
from dalme_app.models import Task, TaskList
from ._common import DALMEBaseViewSet
from dalme_api.filters import TaskFilter


class Tasks(DALMEBaseViewSet):
    """ API endpoint for managing tasks """
    permission_classes = (TaskAccessPolicy,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'title', 'description', 'completed', 'creation_user', 'creation_timestamp', 'assigned_to']
    ordering = ['id']

    @action(detail=True, methods=['patch'])
    def set_state(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            action = self.request.data['action']
            if action == 'mark_done':
                obj.completed = True
                obj.save(update_fields=['completed', 'modification_user', 'modification_timestamp'])
            elif action == 'mark_undone':
                obj.completed = False
                obj.save(update_fields=['completed', 'modification_user', 'modification_timestamp'])
            result = {'message': 'Update successful.'}
            status = 201
        except Exception as e:
            result = {'error': str(e)}
            status = 400
        return Response(result, status)


class TaskLists(DALMEBaseViewSet):
    """ API endpoint for managing tasks lists """
    permission_classes = (TaskListAccessPolicy,)
    queryset = TaskList.objects.all().annotate(task_count=Count('task'))
    serializer_class = TaskListSerializer
