import json
from rest_framework.response import Response
from rest_framework.decorators import action
from dalme_api.serializers import PageSerializer
from dalme_app.models import Page
from dalme_api.access_policies import PageAccessPolicy
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

    @action(detail=True, methods=['post', 'get'])
    def get_manifest(self, request, *args, **kwargs):
        page = self.get_object()
        if page.dam_id is not None:
            try:
                canvas = json.loads(page.get_canvas())
                result = {
                  "@context": "http://iiif.io/api/presentation/2/context.json",
                  "@id": page.get_absolute_url(),
                  "@type": "sc:Manifest",
                  "label": page.name,
                  "metadata": [],
                  "description": [{
                    "@value": f"Manifest for {page.name}",
                    "@language": "en"
                  }],
                  "license": "https://creativecommons.org/licenses/by/3.0/",
                  "attribution": "DALME",
                  "thumbnail": {
                    "@id": f"https://dam.dalme.org/loris/{page.dam_id}/full/thm/0/default.jpg",
                    "@type": "dctypes:Image",
                    "height": 150,
                    "width": 56,
                    "format": "image/jpeg",
                    "service": {
                      "@context": "http://iiif.io/api/image/2/context.json",
                      "@id": f"https://dam.dalme.org/loris/{page.dam_id}",
                      "profile": "http://iiif.io/api/image/2/level1.json"
                    }
                  },
                  "sequences": [
                    {
                      "@id": page.id,
                      "@type": "sc:Canvas",
                      "label": "Folio",
                      "canvases": [canvas]
                    }
                  ],
                  "structures": []
                }
                status = 201

            except Exception as e:
                result = {'error': str(e)}
                status = 400

        else:
            result = {'error': 'This page does not have an image associated in the DAM'}
            status = 400

        return Response(result, status)
