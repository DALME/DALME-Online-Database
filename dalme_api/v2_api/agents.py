from dalme_api import api


class Agents(api.Agents):
    """Endpoint for the Agent resource."""

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs_as = self.request.GET.get('as')
        if qs_as:
            if qs_as == 'credits':
                qs = qs.filter(user__isnull=False)
            if qs_as == 'named':
                qs = qs.filter(user__isnull=True)
        return qs
