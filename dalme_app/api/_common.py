import json
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

    # @action(detail=True, methods=['patch'])
    # def change_owner(self, request, *args, **kwargs):
    #     object = self.get_object()
    #     try:
    #         new_owner = self.request.POST['new_owner']
    #         object.owner = new_owner
    #         object.save(update_fields=['owner', 'modification_user', 'modification_timestamp'])
    #         result = {'message': 'Owner changed succesfully.'}
    #         status = 201
    #     except Exception as e:
    #         result = {'error': str(e)}
    #         status = 400
    #     return Response(result, status)

    def list(self, request, *args, **kwargs):
        full_queryset = self.get_queryset()
        queryset = self.filter_queryset(full_queryset)
        if request.GET.get('data') is not None:
            dt_request = json.loads(request.GET['data'])
            page = self.paginate_queryset(queryset, dt_request.get('start'), dt_request.get('length'))
            serializer = self.get_serializer(page, many=True)
            result = {
                'draw': int(dt_request.get('draw')),  # cast return "draw" value as INT to prevent Cross Site Scripting (XSS) attacks
                'recordsTotal': full_queryset.count(),
                'recordsFiltered': queryset.count(),
                'data': serializer.data
                }
        else:
            serializer = self.get_serializer(queryset, many=True)
            result = serializer.data
        return Response(result)

    def paginate_queryset(self, queryset, start, length):
        if start is not None and length is not None:
            page = queryset[start:start+length]
            if page is not None:
                queryset = page
        return queryset

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
