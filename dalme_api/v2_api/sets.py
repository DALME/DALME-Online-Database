from dalme_api import api
from dalme_app.models import Set

from rest_framework import serializers


class Sets(api.Sets):
    """Endpoint for the Set resource."""

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.GET.get('owner'):
            qs = qs.filter(owner__id=self.request.GET['owner'])
        return qs
