from rest_framework.decorators import action
from rest_framework.response import Response

from dalme_api.access_policies import TaskAccessPolicy, TaskListAccessPolicy
from dalme_api.filters import TaskFilter
from dalme_api.serializers import TaskListSerializer, TaskSerializer
from dalme_app.models import Task, TaskList

from .base_viewset import DALMEBaseViewSet


class Tasks(DALMEBaseViewSet):
    """API endpoint for managing tasks."""

    permission_classes = (TaskAccessPolicy,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'title', 'description', 'completed', 'creation_user', 'creation_timestamp']
    ordering = ['id']

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
