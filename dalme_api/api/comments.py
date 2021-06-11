from django.apps import apps
from django.core.exceptions import ValidationError

from rest_framework import viewsets
from rest_framework.response import Response
from dalme_api.serializers import CommentSerializer
from dalme_app.models import Comment
from dalme_api.access_policies import CommentAccessPolicy
from dalme_app.models import *


class Comments(viewsets.ModelViewSet):
    """ API endpoint for managing comments """
    permission_classes = (CommentAccessPolicy,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self, *args, **kwargs):
        if self.request.GET.get('model') is not None and self.request.GET.get('object') is not None:
            model = apps.get_model(app_label='dalme_app', model_name=self.request.GET['model'])
            obj_pk = self.request.GET['object']
            if isinstance(obj_pk, str):
                obj_pk = int(obj_pk)
            instance = model.objects.get(pk=obj_pk)
            return instance.comments.all()
        return self.queryset

    def create(self, request, *args, **kwargs):
        result = {}
        data = request.data
        try:
            model = apps.get_model(app_label='dalme_app', model_name=data['model'])
            content_object = model.objects.get(pk=int(data['object']))
            body = data['body']
            if not body:
                raise ValidationError("Comment body can't be empty")
            new_comment = content_object.comments.create(body=body)
            serializer = self.get_serializer(new_comment)
            result = serializer.data
            status = 201
        except Exception as e:
            result = str(e)
            status = 400
        return Response(result, status)
