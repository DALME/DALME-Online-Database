class Agents(DALMEBaseViewSet):
    """ API endpoint for managing agents """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    filterset_fields = ['id', 'type']
    search_fields = ['id', 'standard_name', 'notes']
    ordering_fields = ['id', 'standard_name', 'type']
    ordering = ['type', 'standard_name']
