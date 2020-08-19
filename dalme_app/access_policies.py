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


class SourceAccessPolicy(BaseAccessPolicy):
    ''' Manages access policies for Sources endpoint '''

    id = 'sources-policy'

    # @classmethod
    # def scope_queryset(cls, request, queryset):
    #     if request.user.groups.filter(name='Administrators').exists():
    #         return queryset
    #
    #     return queryset.filter(status='published')
