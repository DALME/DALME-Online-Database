from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from dalme_api.serializers import TranscriptionSerializer
from dalme_app.models import Source_pages, Transcription
from dalme_api.access_policies import TranscriptionAccessPolicy


class Transcriptions(viewsets.ModelViewSet):
    """ API endpoint for managing transcriptions """
    permission_classes = (TranscriptionAccessPolicy,)
    queryset = Transcription.objects.all()
    serializer_class = TranscriptionSerializer

    def create(self, request, format=None):
        data = request.data
        s_data = {'version': data['version'], 'transcription': data['transcription']}
        serializer = TranscriptionSerializer(data=s_data)
        if serializer.is_valid():
            new_obj = serializer.save()
            object = Transcription.objects.get(pk=new_obj.id)
            sp = Source_pages.objects.get(source=data['source'], page=data['page'])
            sp.transcription = object
            sp.save()
            serializer = TranscriptionSerializer(object)
            result = serializer.data
            status = 201
        else:
            result = serializer.errors
            status = 400
        return Response(result, status)

    def update(self, request, pk=None, format=None):
        data = request.data
        object = self.get_object()
        if object.version:
            version = int(object.version)
        else:
            version = 0
        if int(data['version']) > version:
            serializer = TranscriptionSerializer(object, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                serializer = TranscriptionSerializer(object)
                result = serializer.data
                status = 201
            else:
                result = serializer.errors
                status = 400
        else:
            serializer = TranscriptionSerializer(object)
            result = serializer.data
            status = 201
        return Response(result, status)

    @action(detail=True, methods=['get'])
    def check_version(self, request, pk=None):
        object = self.get_object()
        remote_version = request.GET.get('v')
        if not remote_version:
            result = {'error': 'Must submit version for checking.'}
            status = 400
        else:
            try:
                remote_version = int(remote_version)
                local_version = int(object.version) if object.version else 0
                if remote_version == local_version:
                    result = ''
                    status = 200
                elif remote_version < local_version:
                    serializer = TranscriptionSerializer(object)
                    if serializer.is_valid():
                        result = serializer.data
                        status = 205
                else:
                    result = {'error': 'Unknown server error.'}
                    status = 500

            except Exception as e:
                result = {'error': str(e)}
                status = 400

        return Response(result, status)
