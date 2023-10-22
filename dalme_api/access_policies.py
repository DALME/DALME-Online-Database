from rest_access_policy import AccessPolicy, AccessPolicyException
import json
import os


class BaseAccessPolicy(AccessPolicy):
    ''' Base subclass of AccessPolicy to enable loading policy
    statements from external sources '''

    id = 'base-policy'
    test_object = None

    def _evaluate_statements(self, statements, request, view, action):
        result = super()._evaluate_statements(statements, request, view, action)
        if not result:
            if self.test_object is not None and hasattr(self.test_object, 'name'):
                self.message = 'You do not have permission to {} {}'.format(action.replace('bulk_', ''), self.test_object.name)
        return result

    def get_policy_statements(self, request, view):
        statements = os.path.join('dalme_app', 'config', 'policies', self.id + '.json')
        with open(statements, 'r') as policy:
            return json.load(policy)

    def get_view_object(self, view):
        if type(view) is dict:
            self.test_object = view.get('object')
            return view.get('object', {})
        else:
            if hasattr(view, "object"):
                obj = view.object
                self.test_object = obj
                return obj
            elif hasattr(view, "get_object"):
                try:
                    obj = view.get_object()
                    self.test_object = obj
                    return obj
                except AssertionError:
                    objects = []
                    for id in list(view.request.data.keys()):
                        view.kwargs['pk'] = id
                        objects.append(view.get_object())
                    return objects
            else:
                return {}

    def is_owner(self, request, view, action):
        records = self.get_view_object(view) if type(self.get_view_object(view)) == 'list' else [self.get_view_object(view)]
        for record in records:
            try:
                if request.user != record.owner:
                    self.test_object = record
                    return False
            except AttributeError:
                return False
        return True

    def is_creator(self, request, view, action):
        records = self.get_view_object(view) if type(self.get_view_object(view)) == 'list' else [self.get_view_object(view)]
        for record in records:
            try:
                if request.user != record.creation_user:
                    self.test_object = record
                    return False
            except AttributeError:
                return False
        return True


class PublicAccessPolicy(BaseAccessPolicy):
    id = 'public-policy'


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


class LibraryReferenceAccessPolicy(BaseAccessPolicy):
    id = 'libraries-policy'


class LocaleAccessPolicy(BaseAccessPolicy):
    id = 'locales-policy'


class PageAccessPolicy(BaseAccessPolicy):
    id = 'pages-policy'

    def can_edit_parent_source(self, request, view, action):
        record = self.get_view_object(view)
        try:
            return SourceAccessPolicy().has_permission(
                request,
                {'object': record.sources.all()[0].source}
            )
        except: # noqa
            return False


class PlaceAccessPolicy(BaseAccessPolicy):
    id = 'places-policy'


class RightsAccessPolicy(BaseAccessPolicy):
    id = 'rights-policy'


class SourceAccessPolicy(BaseAccessPolicy):
    id = 'sources-policy'

    def in_dataset_usergroup(self, request, view, action):
        records = self.get_view_object(view) if type(self.get_view_object(view)) == 'list' else [self.get_view_object(view)]
        for record in records:
            try:
                ds_ugs = [i.set_id.dataset_usergroup.name for i in record.sets.filter(set_id__set_type=3) if i.set_id.dataset_usergroup is not None]
                usergroups = [i.name for i in request.user.groups.all()]
                if not len(list(set(ds_ugs) & set(usergroups))) > 0:
                    return False
            except: # noqa
                return False
        return True

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


class SessionAccessPolicy(BaseAccessPolicy):
    id = 'session-policy'


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
        except: # noqa
            return False


class TicketAccessPolicy(BaseAccessPolicy):
    id = 'tickets-policy'


class WorkflowAccessPolicy(BaseAccessPolicy):
    id = 'workflow-policy'

    def owns_wf_target(self, request, view, action):
        wf = view.get_object()
        target = wf.source
        return request.user == target.owner

    def in_target_dataset_usergroup(self, request, view, action):
        wf = view.get_object()
        target = wf.source
        try:
            ds_ugs = [i.set_id.dataset_usergroup.name for i in target.sets.filter(set_id__set_type=3) if i.set_id.dataset_usergroup is not None]
            usergroups = [i.name for i in request.user.groups.all()]
            if not len(list(set(ds_ugs) & set(usergroups))) > 0:
                return False
        except: # noqa
            return False

        return True


class UserAccessPolicy(BaseAccessPolicy):
    id = 'users-policy'
