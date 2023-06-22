import json
import pathlib

from rest_framework.decorators import action
from rest_framework.response import Response

from dalme_api.access_policies import PageAccessPolicy
from dalme_api.serializers import PageSerializer
from dalme_app.models import Page

from .base_viewset import DALMEBaseViewSet

with pathlib.Path('static/snippets/iiif_manifest.json').open() as fp:
    MANIFEST = json.load(fp)


class Pages(DALMEBaseViewSet):
    """API endpoint for managing pages."""

    permission_classes = (PageAccessPolicy,)
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    @action(detail=True, methods=['post', 'get'])
    def get_rights(self, request, *args, **kwargs):  # noqa: ARG002
        """Return rights information for page."""
        try:
            return Response({'rights': self.get_object().get_rights()}, 201)
        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)

    @action(detail=True, methods=['post', 'get'])
    def get_manifest(self, request, *args, **kwargs):  # noqa: ARG002
        """Return IIIF manifest for page."""
        page = self.get_object()

        if not page.dam_id:
            return Response({'error': 'This page does not have an associated image in the DAM'}, 400)

        try:
            result = MANIFEST.copy()
            result = MANIFEST.copy()
            result['@id'] = page.get_absolute_url()
            result['label'] = page.name
            result['description'][0]['@value'] = f'Manifest for {page.name}'
            result['thumbnail']['@id'] = f'https://dam.dalme.org/loris/{page.dam_id}/full/thm/0/default.jpg'
            result['thumbnail']['service']['@id'] = f'https://dam.dalme.org/loris/{page.dam_id}'
            result['sequences']['@id'] = page.id
            result['sequences']['canvases'] = [json.loads(page.get_canvas())]
            return Response(result, 201)

        except Exception as e:  # noqa: BLE001
            return Response(str(e), 400)
