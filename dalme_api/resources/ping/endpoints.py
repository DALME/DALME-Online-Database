"""Endpoint for API health check."""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from dalme_api.access_policies import SessionAccessPolicy
from dalme_api.resources.users import UserSerializer


class Ping(viewsets.ViewSet):
    """Determine if the API is up and running."""

    permission_classes = (SessionAccessPolicy,)

    @action(detail=False, methods=['get'])
    def ping(self, request):
        """Respond to ping."""
        if request.user.is_authenticated:
            owner = UserSerializer(request.user, fields=['username', 'id'])
            data = {'status': 'ok', 'user': owner.data}
            return Response(data, 200)
        return Response({'error': 'Not authenticated.'}, 403)
