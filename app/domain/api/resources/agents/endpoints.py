"""API endpoint for managing agents."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from app.access_policies import BaseAccessPolicy
from domain.api.viewsets import BaseViewSet
from domain.models import Agent

from .serializers import AgentSerializer


class AgentAccessPolicy(BaseAccessPolicy):
    """Access policies for the Agents endpoint."""

    id = 'agents-policy'


class Agents(BaseViewSet):
    """API endpoint for managing agents."""

    permission_classes = [AgentAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & AgentAccessPolicy]

    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    filterset_fields = ['id', 'agent_type']
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'name', 'agent_type']
    ordering = ['agent_type', 'name']

    def get_queryset(self, *args, **kwargs):
        """Return different querysets based on agent types."""
        qs = super().get_queryset(*args, **kwargs)
        qs_as = self.request.GET.get('as')
        if qs_as:
            if qs_as == 'credits':
                qs = qs.filter(user__isnull=False)
            if qs_as == 'named':
                qs = qs.filter(user__isnull=True)
        return qs
