"""API endpoint for managing tasks and task lists."""
from rest_framework.decorators import action
from rest_framework.response import Response

from dalme_api.access_policies import BaseAccessPolicy
from dalme_api.base_viewset import DALMEBaseViewSet
from dalme_api.filters import TaskFilter, TasklistFilter
from dalme_app.models import Task, TaskList

from .serializers import TaskListSerializer, TaskSerializer


class TaskAccessPolicy(BaseAccessPolicy):
    """Access policies for Tasks endpoint."""

    id = 'tasks-policy'  # noqa: A003


class TaskListAccessPolicy(BaseAccessPolicy):
    """Access policies for Tasks Lists endpoint."""

    id = 'task_lists-policy'  # noqa: A003


class Tasks(DALMEBaseViewSet):
    """API endpoint for managing tasks."""

    permission_classes = (TaskAccessPolicy,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'title', 'description', 'completed', 'creation_user', 'creation_timestamp']
    ordering = ['-creation_timestamp']

    def list(self, request, *args, **kwargs):  # noqa: A003
        """Override method to include context data."""
        if self.request.query_params.get('user'):
            user = self.request.query_params['user']
            self.context = {
                'total_tasks': Task.objects.all().count(),
                'total_created': Task.objects.filter(creation_user=user, completed=False).count(),
                'total_assigned': Task.objects.filter(assignees=user, completed=False).count(),
                'total_completed': Task.objects.filter(completed_by=user).count(),
            }
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['patch'])
    def set_state(self, request, *args, **kwargs):  # noqa: ARG002
        """Set task state."""
        obj = self.get_object()
        try:
            action = self.request.data['action']
            if action == 'mark_done':
                obj.completed = True
                obj.save(update_fields=['completed', 'modification_user', 'modification_timestamp'])
            elif action == 'mark_undone':
                obj.completed = False
                obj.save(update_fields=['completed', 'modification_user', 'modification_timestamp'])

            return Response({'message': 'Update successful.'}, 201)

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)


class TaskLists(DALMEBaseViewSet):
    """API endpoint for managing tasks lists."""

    permission_classes = (TaskListAccessPolicy,)
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    filterset_class = TasklistFilter
