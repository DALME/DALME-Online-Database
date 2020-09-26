from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import action
from dalme_app.serializers import TaskSerializer, TaskListSerializer
from dalme_app.models import Task, TaskList
from dalme_app.access_policies import GeneralAccessPolicy
from ._common import DALMEBaseViewSet


class Tasks(DALMEBaseViewSet):
    """ API endpoint for managing tasks """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=['patch'])
    def set_state(self, request, *args, **kwargs):
        object = self.get_object()
        try:
            action = self.request.POST['action']
            if action == 'mark_done':
                object.completed = True
                object.save(update_fields=['completed', 'modification_user', 'modification_timestamp'])
            elif action == 'mark_undone':
                object.completed = False
                object.save(update_fields=['completed', 'modification_user', 'modification_timestamp'])
            result = {'message': 'Update succesful.'}
            status = 201
        except Exception as e:
            result = {'error': str(e)}
            status = 400
        return Response(result, status)


class TaskLists(DALMEBaseViewSet):
    """ API endpoint for managing tasks lists """
    permission_classes = (GeneralAccessPolicy,)
    queryset = TaskList.objects.all().annotate(task_count=Count('task'))
    serializer_class = TaskListSerializer
