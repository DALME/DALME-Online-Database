"""API endpoint for managing pages."""

import json
import pathlib

# from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.decorators import action
from rest_framework.response import Response

from api.access_policies import BaseAccessPolicy, RecordAccessPolicy
from api.base_viewset import IDABaseViewSet
from ida.models import Page

from .serializers import PageSerializer

with pathlib.Path('static/snippets/iiif_manifest.json').open() as fp:
    MANIFEST = json.load(fp)


class PageAccessPolicy(BaseAccessPolicy):
    """Access policies for Pages endpoint."""

    id = 'pages-policy'

    def get_parent(self, target):
        """Return page parent object (record)."""
        return (target.records.all()[0].record, RecordAccessPolicy())


class Pages(IDABaseViewSet):
    """API endpoint for managing pages."""

    permission_classes = [PageAccessPolicy]
    # TODO: commented out because it's preventing access to unregistered users from the public frontend
    # this shuould probably be integrated with the overal permissions system, e.g. PageAccessPolicy
    # oauth_permission_classes = [TokenHasReadWriteScope]

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
            result['@id'] = page.get_absolute_url()
            result['label'] = page.name
            result['description'][0]['@value'] = f'Manifest for {page.name}'
            result['thumbnail']['@id'] = f'https://dam.dalme.org/loris/{page.dam_id}/full/thm/0/default.jpg'
            result['thumbnail']['service']['@id'] = f'https://dam.dalme.org/loris/{page.dam_id}'
            result['sequences'][0]['@id'] = page.id
            result['sequences'][0]['canvases'] = [json.loads(page.get_canvas())]
            return Response(result, 201)

        except Exception as e:  # noqa: BLE001
            return Response(str(e), 400)
