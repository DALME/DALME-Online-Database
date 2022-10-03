from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action


class DALMEBaseViewSet(viewsets.ModelViewSet):
    """ Generic viewset. Should be subclassed for specific API endpoints. """

    @action(detail=True, methods=['post'])
    def has_permission(self, request, pk=None):
        pc = self.permission_classes[0]
        pc().has_permission(request, self)
        return Response(200)

    @action(detail=False, methods=['delete'])
    def bulk_remove(self, request, *args, **kwargs):
        try:
            for id in list(request.data.keys()):
                self.kwargs['pk'] = id
                instance = self.get_object()
                instance.delete()
            return Response(200)
        except Exception as e:
            return Response({'error': str(e)}, 400)

    @action(detail=False, methods=['put', 'patch'])
    def bulk_edit(self, request, *args, **kwargs):
        partial = True if request.method == 'PATCH' else False
        results = []
        try:
            for id, props in request.data.items():
                self.kwargs['pk'] = id
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=props, partial=partial)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                results.append(serializer.data)
            return Response({'data': results}, 200)
        except Exception as e:
            return Response({'error': str(e)}, 400)

    def get_renderer_context(self):
        context = {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {}),
            'request': getattr(self, 'request', None),
            'model': self.get_serializer().Meta.model.__name__
            }
        if self.request.GET.get('select_type') is not None:
            context['select_type'] = self.request.GET['select_type']
        return context

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
            }
