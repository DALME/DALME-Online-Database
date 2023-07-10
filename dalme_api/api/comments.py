import contextlib

from rest_framework import viewsets
from rest_framework.response import Response

from django.apps import apps

from dalme_api.access_policies import CommentAccessPolicy
from dalme_api.serializers import CommentSerializer
from dalme_app.models import *  # noqa: F403
from dalme_app.models import Comment


class Comments(viewsets.ModelViewSet):
    """API endpoint for managing comments."""

    permission_classes = (CommentAccessPolicy,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self, *args, **kwargs):  # noqa: ARG002
        """Return generic queryset or queryset for specific model/object."""
        if self.request.GET.get('model') is not None and self.request.GET.get('object') is not None:
            model = apps.get_model(app_label='dalme_app', model_name=self.request.GET['model'])
            obj_pk = self.request.GET['object']
            if isinstance(obj_pk, str):
                with contextlib.suppress(ValueError):
                    obj_pk = int(obj_pk)

            instance = model.objects.get(pk=obj_pk)
            return instance.comments.all()
        return self.queryset

    def create(self, request, *args, **kwargs):  # noqa: ARG002
        """Create comment."""
        for para in ['model', 'object', 'body']:
            if request.data.get(para) is None:
                return Response({'error': f'Parameter "{para}" must be supplied.'}, 400)

        try:
            model = apps.get_model(app_label='dalme_app', model_name=request.data['model'])
            obj_pk = request.data['object']
            body = request.data['body']

            if isinstance(obj_pk, str):
                with contextlib.suppress(ValueError):
                    obj_pk = int(obj_pk)

            content_object = model.objects.get(pk=obj_pk)
            new_comment = content_object.comments.create(body=body)
            serializer = self.get_serializer(new_comment)
            return Response(serializer.data, 201)

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)
