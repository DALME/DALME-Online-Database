"""API endpoint for managing preferences."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import viewsets
from rest_framework.response import Response

from django.http import Http404

from app.access_policies import BaseAccessPolicy
from domain.models import Preference, PreferenceKey

from .serializers import PreferenceSerializer


class PreferenceAccessPolicy(BaseAccessPolicy):
    """Access policies for preferences endpoint."""

    id = 'preferences-policy'


class Preferences(viewsets.ViewSet):
    """API endpoint for managing user preferences."""

    permission_classes = [PreferenceAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & PreferenceAccessPolicy]

    def get_object(self, pk=None):
        """Return the object of the view."""
        try:
            key = PreferenceKey.objects.get(name=pk)
            return Preference.objects.get(user=self.request.user, key=key)
        except Exception as exc:
            msg = 'No preferencematches the given query.'
            raise Http404(msg) from exc

    def list(self, request, format=None):  # noqa: A002, ARG002
        """Retrieve preferences for current user."""
        prefs = Preference.objects.filter(user=request.user)
        serializer = PreferenceSerializer(prefs, many=True)
        return Response(serializer.data, 200)

    def update(self, request, pk=None):
        """Update preference."""
        value = request.data.get('value')
        if not pk or value is None:
            return Response({'error': 'Request missing key or data.'}, 400)
        obj = self.get_object(pk)
        obj.data = value
        obj.save()
        return Response(200)
