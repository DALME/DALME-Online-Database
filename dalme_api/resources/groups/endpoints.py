"""API endpoint for managing user groups."""
from oauth2_provider.contrib.rest_framework import TokenHasScope

from dalme_api.access_policies import GeneralAccessPolicy
from dalme_api.base_viewset import DALMEBaseViewSet

from .serializers import GroupSerializer


class Groups(DALMEBaseViewSet):
    """API endpoint for managing user groups."""

    serializer_class = GroupSerializer

    permission_classes = [GeneralAccessPolicy, TokenHasScope]
    required_scopes = ['groups']

    filterset_fields = [
        'id',
        'name',
        'properties__group_type',
        'properties__tenant',
    ]
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    ordering = ['name']

    # TODO: Reactivate when Group/Tenant issues are resolved.
    # def get_queryset(self):
    #     """Make sure that groups are correctly filtered over tenants."""
    #     # TODO: This might not be exactly what we want finally (perhaps we'd
    #     # want to see groups from all tenants in some cases) but let's just
    #     # get it in place for the time being until we have accurate specs.
    #     tenant = get_current_tenant()
    #     q = Q(properties__tenant__pk=tenant.pk) | Q(properties__tenant__pk__isnull=True)
    #     return self.request.user.groups.filter(q)
