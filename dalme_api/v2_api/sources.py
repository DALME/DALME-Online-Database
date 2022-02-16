from dalme_api import api
from dalme_api.v2_serializers import SourceOptionsSerializer


class Sources(api.Sources):
    """Endpoint for the Source resource."""

    @property
    def use_options(self):
        q_as = self.request.GET.get('as')
        return q_as == 'options'

    def get_serializer_class(self):
        if self.use_options:
            return SourceOptionsSerializer
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        if self.use_options:
            serializer_class = self.get_serializer_class()
            kwargs.setdefault('context', self.get_serializer_context())
            return serializer_class(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        if self.use_options:
            # Skips any prefectching here for the most minimal payload possible
            # to load into UI widgets.
            if self.request.GET.get('class'):
                qs = self.get_queryset_by_source_type()
            else:
                qs = Source.objects.all()
            return qs.values('id', 'name')
        return super().get_queryset(*args, **kwargs)
