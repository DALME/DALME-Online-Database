from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from dalme_api.access_policies import SessionAccessPolicy
from dalme_api.serializers.users import UserSerializer


class Session(viewsets.ViewSet):
    """API endpoint for managing user sessions."""

    permission_classes = (SessionAccessPolicy,)

    def retrieve(self, request, pk=None):  # noqa: ARG002
        """Return session."""
        if request.user.is_authenticated:
            # TODO: Fix profile and add full_name here...
            owner = UserSerializer(request.user, fields=['username', 'id'])
            is_admin = any(group.name == "Administrators" for group in request.user.groups.all())
            data = owner.data
            data["is_admin"] = is_admin
            return Response(data, 200)

        return Response({'error': 'Not authenticated.'}, 403)

    @action(detail=False, methods=['post'])
    def alter(self, request):
        """Update session."""
        if not request.data:
            return Response({'error': 'Data missing from request.'}, 400)

        result = []
        for key, value in request.data.items():
            if not value:
                try:
                    del request.session[key]
                    result.append({'key': key, 'result': 'deleted'})
                except KeyError:
                    result.append({'key': key, 'result': 'skipped - does not exist'})
            else:
                request.session[key] = value
                result.append({'key': key, 'result': f'new value: {value}'})

        return Response(result, 201)
