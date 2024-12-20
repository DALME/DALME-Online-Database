"""API endpoint for managing records."""

import json
import pathlib

from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from django.conf import settings

from api.access_policies import RecordAccessPolicy, WebAccessPolicy
from api.base_viewset import IDABaseViewSet
from api.paginators import IDAPageNumberPagination
from domain.filters import RecordFilter
from domain.models import Record

from .serializers import RecordSerializer

with pathlib.Path('static/snippets/iiif_manifest.json').open() as fp:
    MANIFEST = json.load(fp)


class Records(IDABaseViewSet):
    """API endpoint for managing records."""

    permission_classes = [RecordAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & RecordAccessPolicy]

    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    filterset_class = RecordFilter
    search_fields = ['name', 'short_name']

    @action(detail=True, methods=['post', 'get'])
    def get_manifest(self, request, *args, **kwargs):  # noqa: ARG002
        """Return IIIF manifest for the record."""
        record = self.get_object()
        pages = record.pages.all()
        dam_id_list = [page.dam_id for page in pages]

        if not pages:
            return Response({'error': 'This record has no associated pages.'}, 400)

        if len(dam_id_list) == 0:
            return Response({'error': 'The pages in this record have no associated images in the DAM'}, 400)

        try:
            result = MANIFEST.copy()
            result['@id'] = record.get_absolute_url()
            result['label'] = record.name
            result['description'][0]['@value'] = f'Manifest for {record.name}'
            result['thumbnail']['@id'] = f'{settings.DAM_URL}/loris/{dam_id_list[0]}/full/thm/0/default.jpg'
            result['thumbnail']['service']['@id'] = f'{settings.DAM_URL}/loris/{dam_id_list[0]}'
            result['sequences']['@id'] = record.id
            result['sequences']['canvases'] = [json.loads(page.get_canvas()) for page in pages]
            return Response(result, 201)

        except Exception as e:  # noqa: BLE001
            return Response(str(e), 400)


class WebRecords(Records):
    """API endpoint for managing records for frontend apps."""

    queryset = Record.objects.filter(workflow__is_public=True)
    permission_classes = [WebAccessPolicy]
    pagination_class = IDAPageNumberPagination
    renderer_classes = [CamelCaseJSONRenderer]
    authentication_classes = [SessionAuthentication]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        kwargs['field_set'] = ['public', 'images'] if self.request.GET.get('thumbs') else 'public'
        return serializer_class(*args, **kwargs)
