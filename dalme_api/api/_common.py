from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action


class DALMEBaseViewSet(viewsets.ModelViewSet):
    """ Generic viewset. Should be subclassed for specific API endpoints. """

    @action(detail=True, methods=['post'])
    def has_permission(self, request, pk=None):
        pc = self.permission_classes[0]  # type: ignore
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

    @action(detail=False, methods=['patch'])
    def inline_update(self, request, *args, **kwargs):
        pks = [str(pk) for pk in request.data.keys()]
        for pk in pks:
            obj = self.queryset.filter(pk=pk)  # type: ignore
            obj_data = request.data[pk]

            # Update fields.
            # Temporary until sorting out api parser/renderer.
            # from stringcase import snakecase
            # fields = {
            #     snakecase(field): value for field, value in obj_data.items()
            #     if not isinstance(value, dict)
            # }
            # fields = {
            #     field: value for field, value in obj_data.items()
            #     if not isinstance(value, dict)
            # }
            obj.update(**obj_data)

            # Update foreign keys.
            # related = {
            #     fk_field: value
            #     for fk_field, value in obj_data.items()
            #     if fk_field not in fields
            # }

            # for fk_field, value in related.items():
            #     RelatedModel = Place._meta.get_field(fk_field).rel.to
            #     instance = RelatedModel.objects.get(pk=value.id)
            #     obj.update(fk_field=instance)

        return Response({'message': f'Updated {len(pks)} rows.'}, 201)

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
        return serializer_class(*args, **kwargs)  # type: ignore

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
