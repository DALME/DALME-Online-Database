from rest_access_policy import AccessPolicy
import json
import os


class BaseAccessPolicy(AccessPolicy):
    ''' Base subclass of AccessPolicy to enable loading policy
    statements from external sources '''

    id = 'base-policy'

    def get_policy_statements(self, request, view):
        statements = os.path.join('dalme_app', 'config', 'policies', self.id + '.json')
        with open(statements, 'r') as policy:
            return json.load(policy)

    def is_owner(self, request, view, action):
        record = view.get_object()
        return request.user == record.owner


class ConfigsAccessPolicy(BaseAccessPolicy):
    ''' Manages access policies for configs endpoint '''
    id = 'configs-policy'


class GeneralAccessPolicy(BaseAccessPolicy):
    ''' Manages general access policies for all endpoints '''
    id = 'general-policy'


class ImageAccessPolicy(BaseAccessPolicy):
    ''' Manages general access policies for Images endpoint'''
    id = 'images-policy'


class SourceAccessPolicy(BaseAccessPolicy):
    ''' Manages access policies for Sources endpoint '''
    id = 'sources-policy'

    def in_dataset_usergroup(self, request, view, action):
        record = view.get_object()
        if record.sets.filter(set_id__set_type=3).exists():
            ds_ugs = [i.set_id.dataset_usergroup.name for i in record.sets.filter(set_id__set_type=3) if i.set_id.dataset_usergroup is not None]
            usergroups = [i.name for i in request.user.groups.all()]
            return len(list(set(ds_ugs) & set(usergroups))) > 0
        else:
            return False


class SetAccessPolicy(BaseAccessPolicy):
    ''' Manages access policies for Sets endpoint '''
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


class WorkflowAccessPolicy(BaseAccessPolicy):
    ''' Manages access policies for Sets endpoint '''
    id = 'workflow-policy'

    def owns_wf_target(self, request, view, action):
        wf = view.get_object()
        target = wf.source
        return request.user == target.owner


class UserAccessPolicy(BaseAccessPolicy):
    ''' Manages access policies for users/profiles endpoint '''
    id = 'user-policy'
