from rest_framework.response import Response
from rest_framework.decorators import action
from dalme_app.serializers import PageSerializer
from dalme_app.models import Page
from dalme_app.access_policies import PageAccessPolicy
from ._common import DALMEBaseViewSet


class Pages(DALMEBaseViewSet):
    """ API endpoint for managing pages """
    permission_classes = (PageAccessPolicy,)
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    @action(detail=True, methods=['post', 'get'])
    def get_rights(self, request, *args, **kwargs):
        object = self.get_object()
        try:
            result = {'rights': object.get_rights()}
            status = 201
        except Exception as e:
            result = {'error': str(e)}
            status = 400
        return Response(result, status)
