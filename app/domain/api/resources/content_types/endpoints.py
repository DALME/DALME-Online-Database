"""API endpoint for managing content types."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.generics import get_object_or_404

from app.access_policies import GeneralAccessPolicy
from domain.api.viewsets import BaseViewSet
from domain.models import ContentTypeExtended

from .filters import ContentTypeFilter
from .serializers import (
    ContentTypeSerializer,
)


class ContentTypes(BaseViewSet):
    """API endpoint for managing ContentTypes."""

    permission_classes = [GeneralAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & GeneralAccessPolicy]

    queryset = ContentTypeExtended.objects.all()
    serializer_class = ContentTypeSerializer
    filterset_class = ContentTypeFilter

    def get_object(self):
        """Return the object the view is displaying when requested by either id or model name."""
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg in self.kwargs:
            lookup_value = self.kwargs[lookup_url_kwarg]
            if not str(lookup_value).isdigit():
                filter_kwargs = {'model': lookup_value}
                obj = get_object_or_404(self.queryset, **filter_kwargs)
                self.check_object_permissions(self.request, obj)
                return obj
        return super().get_object()
