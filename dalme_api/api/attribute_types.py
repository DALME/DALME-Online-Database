from django.db.models import Q
from dalme_api.serializers import AttributeTypeSerializer, ContentXAttributeSerializer
from dalme_app.models import Attribute_type, Content_attributes
from dalme_api.access_policies import GeneralAccessPolicy
from ._common import DALMEBaseViewSet


class AttributeTypes(DALMEBaseViewSet):
    """ API endpoint for managing attribute types """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Attribute_type.objects.all()
    serializer_class = AttributeTypeSerializer

    def get_queryset(self, *args, **kwargs):
        if self.request.GET.get('filter') is not None:
            filter_v = self.request.GET['filter'].split(',')
            filter_q = Q(**{filter_v[0]: filter_v[1]})
            return Content_attributes.objects.filter(filter_q)
        return super().get_queryset(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.GET.get('filter') is not None:
            if self.request.GET['filter'].split(',')[0] == 'content_type':
                return ContentXAttributeSerializer
        return super().get_serializer_class()
