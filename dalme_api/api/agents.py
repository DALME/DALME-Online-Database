from dalme_api.access_policies import AgentAccessPolicy
from dalme_api.serializers import AgentSerializer
from dalme_app.models import Agent

from .base_viewset import DALMEBaseViewSet


class Agents(DALMEBaseViewSet):
    """API endpoint for managing agents."""

    permission_classes = (AgentAccessPolicy,)
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
