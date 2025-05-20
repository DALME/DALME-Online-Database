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


class Preferences(viewsets.ModelViewSet):
    """API endpoint for managing user preferences."""

    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer
    permission_classes = [PreferenceAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & PreferenceAccessPolicy]

    def get_object(self):
        """Return the object of the view."""
        pk = self.kwargs.get('pk')
        if not pk:
            return None
        try:
            key = PreferenceKey.objects.get(name=pk)
            return Preference.objects.get(user=self.request.user, key=key)
        except Exception as exc:
            msg = 'No preference matches the given query.'
            raise Http404(msg) from exc

    def get_queryset(self):
        """Return the queryset of the view filtered by user."""
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

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
        obj = self.get_object()
        obj.data = value
        obj.save()
        serializer = PreferenceSerializer(self.queryset.get(pk=obj.id))
        return Response(serializer.data, 200)
