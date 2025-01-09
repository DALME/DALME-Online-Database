"""API endpoint for managing the record editor."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import viewsets
from rest_framework.response import Response

from app.access_policies import BaseAccessPolicy
from domain.api.resources.editor.serializers import ElementSerializer, ElementSetSerializer
from domain.models import ElementSet


class EditorAccessPolicy(BaseAccessPolicy):
    """Access policies for the Editor endpoint."""

    id = 'editor-policy'


class ElementSets(viewsets.ViewSet):
    """Retrieve TEI element sets for the editor."""

    permission_classes = [EditorAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & EditorAccessPolicy]

    def list(self, request):  # noqa: ARG002
        # user = request.user
        # TODO: filter qs to include owned sets + relevant project sets
        element_sets = ElementSet.objects.all()
        elements = [e.elements.all() for e in element_sets]
        elements = list({e for sl in elements for e in sl})
        set_serializer = ElementSetSerializer(element_sets, many=True)
        element_serializer = ElementSerializer(elements, many=True)
        return Response(
            {
                'sets': set_serializer.data,
                'elements': element_serializer.data,
            },
            200,
        )
