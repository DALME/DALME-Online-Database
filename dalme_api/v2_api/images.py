from rest_framework.response import Response

from dalme_api import api
from dalme_api.v2_serializers import ImageOptionsSerializer


class Images(api.Images):
    """Endpoint for the Image resource."""

    @property
    def options_view(self):
        q_as = self.request.GET.get('as')
        return q_as == 'options'

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if self.options_view:
            serializer_class = ImageOptionsSerializer
        return serializer_class

    def get_serializer(self, *args, **kwargs):
        if self.options_view:
            serializer_class = self.get_serializer_class()
            kwargs.setdefault('context', self.get_serializer_context())
            return serializer_class(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.options_view:
            qs = qs.values('ref', 'field8')
        return qs

    # NOTE: Needs override as the v1 logic doesn't respect the MRO correctly.
    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        result = self.get_serializer(qs, many=True)
        return Response(result.data)
