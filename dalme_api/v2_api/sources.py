from dalme_api import api
from dalme_api.v2_serializers import SourceOptionsSerializer
from dalme_app.models import Source


class Sources(api.Sources):
    """Endpoint for the Source resource."""

    @property
    def options_view(self):
        q_as = self.request.GET.get('as')
        return q_as == 'options'

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if self.options_view:
            serializer_class = SourceOptionsSerializer
        return serializer_class

    def get_serializer(self, *args, **kwargs):
        if self.options_view:
            serializer_class = self.get_serializer_class()
            kwargs.setdefault('context', self.get_serializer_context())
            return serializer_class(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        if self.options_view:
            # Skips any prefectching here for the most minimal payload possible
            # to load into UI widgets.
            if self.request.GET.get('class'):
                qs = self.get_queryset_by_source_type()
            else:
                qs = Source.objects.all()
            return qs.values('id', 'name')
        return super().get_queryset(*args, **kwargs)