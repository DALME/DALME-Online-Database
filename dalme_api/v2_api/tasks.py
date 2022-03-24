from dalme_api import api


class Tasks(api.Tasks):
    """Endpoint for the Task resource."""

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.GET.get('assigned_to'):
            qs = qs.filter(assigned_to__id=self.request.GET['assigned_to'])
        return qs
