"""API endpoint for managing workflows."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from django.utils import timezone

from app.access_policies import BaseAccessPolicy, RecordAccessPolicy
from domain.models import Record, Workflow, WorkLog

from .serializers import WorkflowSerializer


class WorkflowAccessPolicy(BaseAccessPolicy):
    """Access policies for Workflow endpoint."""

    id = 'workflow-policy'

    def get_parent(self, target):
        """Return workflow parent object (record)."""
        return (target.record, RecordAccessPolicy())


class Workflows(viewsets.ModelViewSet):
    """API endpoint for managing the project's workflow."""

    permission_classes = [WorkflowAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & WorkflowAccessPolicy]

    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer

    @action(detail=True, methods=['patch'])
    def change_state(self, request, *args, **kwargs):  # noqa: ARG002
        """Change workflow status."""
        obj = self.get_object()
        try:
            action = self.request.data['action']
            stage_dict = dict(Workflow.PROCESSING_STAGES)
            status_dict = dict(Workflow.WORKFLOW_STATUS)
            if action == 'stage_done':
                stage = int(self.request.data['code'])
                stage_name = stage_dict[stage]
                setattr(obj, stage_name + '_done', True)
                obj.last_user = request.user
                obj.last_modified = timezone.now()
                obj.save()
                self.update_log(obj, f'{stage_name}: marked as done')

            elif action == 'begin_stage':
                stage = int(self.request.data['code'])
                stage_name = stage_dict[stage]
                obj.stage = stage
                obj.last_user = request.user
                obj.last_modified = timezone.now()
                obj.save()
                self.update_log(obj, f'{stage_name}: work commenced')

            elif action == 'toggle_help':
                if obj.help_flag:
                    obj.help_flag = False
                else:
                    obj.help_flag = True
                obj.last_user = request.user
                obj.last_modified = timezone.now()
                obj.save()
                self.update_log(obj, f'help flag set to {obj.help_flag}')

            elif action == 'toggle_public':
                if obj.is_public:
                    obj.is_public = False
                else:
                    obj.is_public = True
                obj.last_user = request.user
                obj.last_modified = timezone.now()
                obj.save()
                self.update_log(obj, f'public flag set to {obj.is_public}')

            elif action == 'change_status':
                status = int(self.request.data['code'])
                prev_status = obj.wf_status
                obj.wf_status = status
                obj.last_user = request.user
                obj.last_modified = timezone.now()
                obj.save()
                self.update_log(obj, f'status changed from {status_dict[prev_status]} to {status_dict[status]}')

            serializer = WorkflowSerializer(obj)
            return Response(serializer.data, 200)

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)

    def update_log(self, record, message):
        """Update associated work log."""
        WorkLog.objects.create(record=record, event=message)

    def get_object(self):
        """Return the object the view is displaying when provided a record id."""
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        queryset = Record.unattributed.all()
        filter_kwargs = {'pk': lookup_value}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj.workflow
