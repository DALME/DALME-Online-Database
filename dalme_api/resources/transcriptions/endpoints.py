"""API endpoint for managing transcriptions."""
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from dalme_api.access_policies import BaseAccessPolicy, RecordAccessPolicy
from ida.models import Folio, Transcription

from .serializers import TranscriptionSerializer


class TranscriptionAccessPolicy(BaseAccessPolicy):
    """Access policies for Transcriptions endpoint."""

    id = 'transcriptions-policy'  # noqa: A003

    def get_parent(self, target):
        """Return transcription parent object (record)."""
        return (target.folios.all()[0].record, RecordAccessPolicy())


class Transcriptions(viewsets.ModelViewSet):
    """API endpoint for managing transcriptions."""

    permission_classes = [TranscriptionAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope]

    queryset = Transcription.objects.all()
    serializer_class = TranscriptionSerializer

    def create(self, request, fmt=None):  # noqa: ARG002
        """Create new transcription."""
        serializer_data = {'version': request.data['version'], 'transcription': request.data['transcription']}
        serializer = TranscriptionSerializer(data=serializer_data)
        if serializer.is_valid():
            new_obj = serializer.save()
            obj = Transcription.objects.get(pk=new_obj.id)
            sp = Folio.objects.get(record=request.data['record'], page=request.data['page'])
            sp.transcription = obj
            sp.save()
            serializer = TranscriptionSerializer(obj)
            return Response(serializer.data, 201)
        return Response(serializer.errors, 400)

    def update(self, request, pk=None, fmt=None):  # noqa: ARG002
        """Update existing transcription."""
        obj = self.get_object()
        version = int(obj.version) if obj.version else 0
        if int(request.data['version']) > version:
            serializer = TranscriptionSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                serializer = TranscriptionSerializer(obj)
                return Response(serializer.data, 201)
            return Response(serializer.errors, 400)

        serializer = TranscriptionSerializer(obj)
        return Response(serializer.data, 201)

    @action(detail=True, methods=['get'])
    def check_version(self, request, pk=None):  # noqa: ARG002
        """Check transcription version."""
        obj = self.get_object()
        remote_version = request.GET.get('v')

        if not remote_version:
            return Response({'error': 'Must submit version for checking.'}, 400)

        try:
            remote_version = int(remote_version)
            local_version = int(obj.version) if obj.version else 0
            if remote_version == local_version:
                return Response(200)

            if remote_version < local_version:
                serializer = TranscriptionSerializer(obj)
                if serializer.is_valid():
                    return Response(serializer.data, 205)

            return Response({'error': 'Unknown server error.'}, 500)

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)
