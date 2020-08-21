from rest_access_policy import AccessPolicy
import json
import os


class BaseAccessPolicy(AccessPolicy):
    ''' Base subclass of AccessPolicy to enable loading policy
    statements from external sources '''

    id = 'base-policy'

    def get_policy_statements(self, request, view):
        statements = os.path.join('dalme_app', 'policies', self.id + '.json')
        with open(statements, 'r') as policy:
            return json.load(policy)

    def is_owner(self, request, view, action):
        record = view.get_object()
        return request.user == record.owner

    def owns_wf_target(self, request, view, action):
        wf = view.get_object()
        target = wf.source
        return request.user == target.owner

    def can_view(self, request, view, action):
        record = view.get_object()
        return request.user == record.owner or record.permissions != 1

    def can_add(self, request, view, action):
        record = view.get_object()
        return request.user == record.owner or record.permissions > 2

    def can_delete(self, request, view, action):
        record = view.get_object()
        return request.user == record.owner or record.permissions == 4


class GeneralAccessPolicy(BaseAccessPolicy):
    ''' Manages general access policies for all endpoints '''
    id = 'general-policy'


class SourceAccessPolicy(BaseAccessPolicy):
    ''' Manages access policies for Sources endpoint '''
    id = 'sources-policy'


class SetAccessPolicy(BaseAccessPolicy):
    ''' Manages access policies for Sets endpoint '''
    id = 'sets-policy'


class WorkflowAccessPolicy(BaseAccessPolicy):
    ''' Manages access policies for Sets endpoint '''
    id = 'workflow-policy'
