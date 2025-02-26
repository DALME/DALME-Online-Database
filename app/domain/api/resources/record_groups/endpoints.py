"""API endpoint for managing record groups."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from app.access_policies import RecordAccessPolicy
from domain.api.viewsets import BaseViewSet
from domain.models import RecordGroup

from .serializers import RecordGroupSerializer


class RecordGroups(BaseViewSet):
    """API endpoint for managing record groups."""

    permission_classes = [RecordAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & RecordAccessPolicy]

    queryset = RecordGroup.objects.all()
    serializer_class = RecordGroupSerializer
    search_fields = ['name', 'short_name']
