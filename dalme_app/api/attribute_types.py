from django.db.models import Q
from dalme_app.serializers import AttributeTypeSerializer, ContentXAttributeSerializer
from dalme_app.models import Attribute_type, Content_attributes
from dalme_app.access_policies import GeneralAccessPolicy
from ._common import DALMEBaseViewSet


class AttributeTypes(DALMEBaseViewSet):
    """ API endpoint for managing attribute types """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Attribute_type.objects.all()
    serializer_class = AttributeTypeSerializer

    def get_queryset(self, *args, **kwargs):
        if self.request.GET.get('filter') is not None:
            filter = self.request.GET['filter'].split(',')
            filter_q = Q(**{filter[0]: filter[1]})
            queryset = Content_attributes.objects.filter(filter_q)
        else:
            queryset = Attribute_type.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.request.GET.get('filter') is not None and self.request.GET['filter'].split(',')[0] == 'content_type':
            serializer = ContentXAttributeSerializer
        else:
            serializer = self.serializer_class
        return serializer
