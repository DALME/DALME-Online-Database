from stringcase import snakecase

from django.db.models import Q

from dalme_api.access_policies import GeneralAccessPolicy
from dalme_api.serializers import AttributeTypeSerializer, ContentAttributesSerializer
from dalme_app.models import AttributeType, ContentAttributes

from .base_viewset import DALMEBaseViewSet


class AttributeTypes(DALMEBaseViewSet):
    """API endpoint for managing attribute types."""

    permission_classes = (GeneralAccessPolicy,)
    queryset = AttributeType.objects.all()
    serializer_class = AttributeTypeSerializer

    def get_queryset(self, *args, **kwargs):
        """Return filtered querysets."""
        if self.request.GET.get('short_names') is not None:
            q_short_names = self.request.GET.get('short_names')
            q_short_names = [snakecase(short_name) for short_name in q_short_names.split(',')]
            return AttributeType.objects.filter(short_name__in=q_short_names)

        if self.request.GET.get('filter') is not None:
            filter_v = self.request.GET['filter'].split(',')
            filter_q = Q(**{filter_v[0]: filter_v[1]})
            return ContentAttributes.objects.filter(filter_q)

        return super().get_queryset(*args, **kwargs)

    def get_serializer_class(self):
        """Return serializer class."""
        if self.request.GET.get('filter') is not None and self.request.GET['filter'].split(',')[0] == 'content_type':
            return ContentAttributesSerializer
        return super().get_serializer_class()
