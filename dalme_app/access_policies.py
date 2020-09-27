from rest_access_policy import AccessPolicy, AccessPolicyException
import json
import os
from django.views.generic import DetailView
from dalme_app.models import Source


class BaseAccessPolicy(AccessPolicy):
    ''' Base subclass of AccessPolicy to enable loading policy
    statements from external sources '''

    id = 'base-policy'

    def get_policy_statements(self, request, view):
        statements = os.path.join('dalme_app', 'config', 'policies', self.id + '.json')
        with open(statements, 'r') as policy:
            return json.load(policy)

    @staticmethod
    def get_view_object(view):
        if type(view) is dict:
            return view.get('object', {})
        else:
            if hasattr(view, "object"):
                return view.object
            elif hasattr(view, "get_object"):
                return view.get_object()
            else:
                return {}

    def is_owner(self, request, view, action):
        record = self.get_view_object(view)
        try:
            return request.user == record.owner
        except AttributeError:
            return False

    def is_creator(self, request, view, action):
        record = self.get_view_object(view)
        try:
            return request.user == record.creation_user
        except AttributeError:
            return False


class AgentAccessPolicy(BaseAccessPolicy):
    id = 'agents-policy'


class AttachmentAccessPolicy(BaseAccessPolicy):
    id = 'attachments-policy'


class ChoicesAccessPolicy(BaseAccessPolicy):
    id = 'choices-policy'


class CommentAccessPolicy(BaseAccessPolicy):
    id = 'comments-policy'


class ConfigsAccessPolicy(BaseAccessPolicy):
    id = 'configs-policy'


class GeneralAccessPolicy(BaseAccessPolicy):
    id = 'general-policy'


class ImageAccessPolicy(BaseAccessPolicy):
    id = 'images-policy'


class PageAccessPolicy(BaseAccessPolicy):
    id = 'pages-policy'

    def can_edit_parent_source(self, request, view, action):
        record = self.get_view_object(view)
        try:
            return SourceAccessPolicy().has_permission(
                request,
                {'object': record.sources.all()[0].source}
            )
        except:
            return False


class RightsAccessPolicy(BaseAccessPolicy):
    id = 'rights-policy'


class SourceAccessPolicy(BaseAccessPolicy):
    id = 'sources-policy'

    def in_dataset_usergroup(self, request, view, action):
        record = self.get_view_object(view)
        try:
            ds_ugs = [i.set_id.dataset_usergroup.name for i in record.sets.filter(set_id__set_type=3) if i.set_id.dataset_usergroup is not None]
            usergroups = [i.name for i in request.user.groups.all()]
            return len(list(set(ds_ugs) & set(usergroups))) > 0
        except:
            return False

    def _get_invoked_action(self, view) -> str:
        if hasattr(view, "action"):
            if view.action == 'has_permission':
                return 'update'
            else:
                return view.action
        elif hasattr(view, "__class__"):
            if view.__class__.__name__ in ['SourceDetail', 'dict']:
                return 'update'
            else:
                return view.__class__.__name__
        raise AccessPolicyException("Could not determine action of request")


class SetAccessPolicy(BaseAccessPolicy):
    id = 'sets-policy'

    def can_view(self, request, view, action):
        record = view.get_object()
        return request.user == record.owner or record.permissions != 1

    def can_add(self, request, view, action):
        record = view.get_object()
        return request.user == record.owner or record.permissions > 2

    def can_delete(self, request, view, action):
        record = view.get_object()
        return request.user == record.owner or record.permissions == 4


class TaskAccessPolicy(BaseAccessPolicy):
    id = 'tasks-policy'


class TaskListAccessPolicy(BaseAccessPolicy):
    id = 'task_lists-policy'


class TranscriptionAccessPolicy(BaseAccessPolicy):
    id = 'transcriptions-policy'

    def can_edit_parent_source(self, request, view, action):
        record = self.get_view_object(view)
        try:
            return SourceAccessPolicy().has_permission(
                request,
                {'object': record.source_pages.all()[0].source}
            )
        except:
            return False


class TicketAccessPolicy(BaseAccessPolicy):
    id = 'tickets-policy'


class WorkflowAccessPolicy(BaseAccessPolicy):
    id = 'workflow-policy'

    def owns_wf_target(self, request, view, action):
        wf = view.get_object()
        target = wf.source
        return request.user == target.owner


class UserAccessPolicy(BaseAccessPolicy):
    id = 'users-policy'
