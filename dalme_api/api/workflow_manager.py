from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from dalme_api.serializers import WorkflowSerializer
from dalme_app.models import Workflow, Work_log
from dalme_api.access_policies import WorkflowAccessPolicy


class WorkflowManager(viewsets.ModelViewSet):
    """ API endpoint for managing the project's workflow """
    permission_classes = (WorkflowAccessPolicy,)
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer

    @action(detail=True, methods=['patch'])
    def change_state(self, request, *args, **kwargs):
        object = self.get_object()
        try:
            result = {}
            action = self.request.data['action']
            stage_dict = dict(Workflow.PROCESSING_STAGES)
            status_dict = dict(Workflow.WORKFLOW_STATUS)
            if action == 'stage_done':
                stage = int(self.request.data['code'])
                stage_name = stage_dict[stage]
                setattr(object, stage_name + '_done', True)
                object.last_user = request.user
                object.last_modified = timezone.now()
                object.save()
                self.update_log(object, stage_name + ': marked as done')
                next_stage = stage + 1
                result['prev_stage_name'] = stage_name
                result['mod_html'] = '<i class="far fa-history fa-fw"></i> Now | <a href="/users/' + request.user.username + '">' + request.user.profile.full_name + '</a>'
                if stage == 4:
                    result['status_html'] = '<div class="wf-manager-status tag-wf-awaiting">awaiting parsing</div>'
                else:
                    result['status_html'] = '<button class="wf-manager-status_btn tag-wf-awaiting" role="button" onclick="update_workflow(\'begin_stage\',' + str(next_stage) + ')">\
                    begin ' + stage_dict[next_stage] + '</button>'
            elif action == 'begin_stage':
                stage = int(self.request.data['code'])
                stage_name = stage_dict[stage]
                object.stage = stage
                object.last_user = request.user
                object.last_modified = timezone.now()
                object.save()
                self.update_log(object, stage_name + ': work commenced')
                result['stage_name'] = stage_name
                result['mod_html'] = '<i class="far fa-history fa-fw"></i> Now | <a href="/users/' + request.user.username + '">' + request.user.profile.full_name + '</a>'
                result['status_html'] = '<div class="wf-manager-status tag-wf-in_progress">' + stage_name + ' in progress</div>\
                <button class="wf-manager-status_btn tag-wf-in_progress" role="button" onclick="update_workflow(\'stage_done\', ' + str(stage) + ')">\
                <i class="far fa-check-square fa-fw"></i> DONE</button>'
            elif action == 'toggle_help':
                if object.help_flag:
                    object.help_flag = False
                else:
                    object.help_flag = True
                object.last_user = request.user
                object.last_modified = timezone.now()
                object.save()
                self.update_log(object, 'help flag set to ' + str(object.help_flag))
            elif action == 'toggle_public':
                if object.is_public:
                    object.is_public = False
                else:
                    object.is_public = True
                object.last_user = request.user
                object.last_modified = timezone.now()
                object.save()
                self.update_log(object, 'public flag set to ' + str(object.is_public))
            elif action == 'change_status':
                status = int(self.request.data['code'])
                prev_status = object.wf_status
                object.wf_status = status
                object.last_user = request.user
                object.last_modified = timezone.now()
                object.save()
                self.update_log(object, 'status changed from "' + status_dict[prev_status] + '" to "' + status_dict[status] + '"')
                status_name = status_dict[status]
                result['mod_html'] = '<i class="far fa-history fa-fw"></i> Now | <a href="/users/' + request.user.username + '">' + request.user.profile.full_name + '</a>'
                if status != 2:
                    result['status_html'] = '<div class="wf-manager-status tag-wf-' + status_name + '">' + status_name + '</div>'
                else:
                    stage = object.stage
                    stage_name = stage_dict[stage]
                    if getattr(object, stage_name + '_done'):
                        if stage == 4:
                            result['status_html'] = '<div class="wf-manager-status tag-wf-awaiting">awaiting parsing</div>'
                        else:
                            next_stage = stage + 1
                            result['status_html'] = '<button class="wf-manager-status_btn tag-wf-awaiting" role="button" onclick="update_workflow(\'begin_stage\', ' + str(next_stage) + ')">\
                            begin ' + stage_dict[next_stage] + '</button>'
                    else:
                        result['status_html'] = '<div class="wf-manager-status tag-wf-in_progress">' + stage_name + ' in progress</div>\
                        <button class="wf-manager-status_btn tag-wf-in_progress" role="button" onclick="update_workflow(\'stage_done\', ' + str(stage) + ')">\
                        <i class="far fa-check-square fa-fw"></i> DONE</button>'
            result['message'] = 'Update succesful.'
            status = 201
        except Exception as e:
            result = {'error': str(e)}
            status = 400
        return Response(result, status)

    def update_log(self, source, message):
        Work_log.objects.create(source=source, event=message)
