"""API endpoint for managing user groups."""
from django.contrib.auth.models import Group

from dalme_api.access_policies import GeneralAccessPolicy
from dalme_api.serializers import GroupSerializer

from .base_viewset import DALMEBaseViewSet


class Groups(DALMEBaseViewSet):
    """API endpoint for managing user groups."""

    permission_classes = (GeneralAccessPolicy,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filterset_fields = ['id', 'name', 'properties__group_type']
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    ordering = ['name']
