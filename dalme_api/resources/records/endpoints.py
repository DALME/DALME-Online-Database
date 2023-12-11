"""API endpoint for managing records."""
import json
import pathlib

from rest_framework.decorators import action
from rest_framework.response import Response

from dalme_api.access_policies import RecordAccessPolicy
from dalme_api.base_viewset import DALMEBaseViewSet
from dalme_api.filters import RecordFilter
from dalme_app.models import Record

from .serializers import RecordSerializer

with pathlib.Path('static/snippets/iiif_manifest.json').open() as fp:
    MANIFEST = json.load(fp)


class Records(DALMEBaseViewSet):
    """API endpoint for managing records."""

    permission_classes = (RecordAccessPolicy,)
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    filterset_class = RecordFilter
    search_fields = ['name', 'short_name']
    ordering_fields = ['name', 'short_name']
    ordering_aggregates = {
        'no_folios': {
            'function': 'Count',
            'expression': 'pages',
        },
    }
    ordering = ['name']

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
            result['thumbnail']['@id'] = f'https://dam.dalme.org/loris/{dam_id_list[0]}/full/thm/0/default.jpg'
            result['thumbnail']['service']['@id'] = f'https://dam.dalme.org/loris/{dam_id_list[0]}'
            result['sequences']['@id'] = record.id
            result['sequences']['canvases'] = [json.loads(page.get_canvas()) for page in pages]
            return Response(result, 201)

        except Exception as e:  # noqa: BLE001
            return Response(str(e), 400)

    def get_queryset(self, *args, **kwargs):  # noqa: ARG002
        """Return filtered queryset."""
        # access_policy = self.permission_classes[0]
        # queryset = access_policy.scope_queryset(self.request, self.queryset)
        # return queryset if self.options_view else queryset.prefetch_related('attributes')
        return (
            self.queryset
            if self.options_view
            else Record.objects.prefetch_related(
                'parent',
                'attributes__attributevaluebool',
                'attributes__attributevaluedate',
                'attributes__attributevaluedec',
                'attributes__attributevaluefkey__value',
                'attributes__attributevalueint',
                'attributes__attributevaluejson',
                'attributes__attributevaluetxt',
                'attributes__attributevaluestr',
                'pages',
                'folios',
                'tags',
            )
        )
