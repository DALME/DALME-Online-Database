from django.db.models import Q
from dalme_api.serializers import AttributeTypeSerializer, ContentXAttributeSerializer
from dalme_app.models import Attribute_type, Content_attributes
from dalme_api.access_policies import GeneralAccessPolicy
from ._common import DALMEBaseViewSet
from rest_framework.decorators import action
from stringcase import snakecase


class AttributeTypes(DALMEBaseViewSet):
    """ API endpoint for managing attribute types """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Attribute_type.objects.all()
    serializer_class = AttributeTypeSerializer

    def get_queryset(self, *args, **kwargs):
        if self.request.GET.get('short_names') is not None:
            q_short_names = self.request.GET.get('short_names')
            q_short_names = [
                snakecase(short_name)
                for short_name in q_short_names.split(',')  # type: ignore
            ]
            return Attribute_type.objects.filter(short_name__in=q_short_names)

        elif self.request.GET.get('filter') is not None:
            filter_v = self.request.GET['filter'].split(',')
            filter_q = Q(**{filter_v[0]: filter_v[1]})
            return Content_attributes.objects.filter(filter_q)

        return super().get_queryset(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.GET.get('filter') is not None:
            if self.request.GET['filter'].split(',')[0] == 'content_type':
                return ContentXAttributeSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'])
    def get_by_shortname(self, request, *args, **kwargs):
        q_short_names = self.request.GET.get('short_names')
        if q_short_names:
            q_short_names = [
                snakecase(short_name)
                for short_name in q_short_names.split(',')
            ]
            return Attribute_type.objects.filter(short_name__in=q_short_names)

        return super().get_queryset(*args, **kwargs)
