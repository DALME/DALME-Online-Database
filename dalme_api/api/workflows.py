"""API endpoint for managing workflows."""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.utils import timezone

from dalme_api.access_policies import WorkflowAccessPolicy
from dalme_api.serializers import WorkflowSerializer
from dalme_app.models import Workflow, WorkLog


class Workflows(viewsets.ModelViewSet):
    """API endpoint for managing the project's workflow."""

    permission_classes = (WorkflowAccessPolicy,)
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer

    @action(detail=True, methods=['patch'])
    def change_state(self, request, *args, **kwargs):  # noqa: ARG002
        """Change workflow status."""
        obj = self.get_obj()
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

            return Response(201)

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)

    def update_log(self, record, message):
        """Update associated work log."""
        WorkLog.objects.create(record=record, event=message)
