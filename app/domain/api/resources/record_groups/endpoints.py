"""API endpoint for managing record groups."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from django.db.models import Q

from app.access_policies import RecordAccessPolicy
from domain.api.viewsets import BaseViewSet
from domain.models import RecordGroup

from .serializers import RecordGroupSerializer


class RecordGroups(BaseViewSet):
    """API endpoint for managing record groups."""

    permission_classes = [RecordAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & RecordAccessPolicy]

    serializer_class = RecordGroupSerializer
    search_fields = ['name', 'short_name']

    def get_queryset(self):
        qs = RecordGroup.unattributed.all() if self.options_view else RecordGroup.objects.all()

        if self.request and hasattr(self.request, 'user'):
            user = self.request.user
            if not user.is_superuser:
                q = Q(is_private=False) & ~Q(owner=user)
                return qs.exclude(q)

        return qs
