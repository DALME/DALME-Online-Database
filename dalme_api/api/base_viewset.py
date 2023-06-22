from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class DALMEBaseViewSet(viewsets.ModelViewSet):
    """Generic viewset. Should be subclassed for specific API endpoints."""

    permission_classes = ()
    queryset = None
    serializer_class = None
    options_serializer_class = None
    url_serializer_class = None

    @property
    def options_view(self):
        """Return boolean indicating whether the request is for options values."""
        q_as = self.request.GET.get('as')
        return q_as == 'options'

    @property
    def url_view(self):
        """Return boolean indicating whether the request is for url values."""
        q_as = self.request.GET.get('as')
        return q_as == 'url'

    @action(detail=True, methods=['post'])
    def has_permission(self, request, pk=None):  # noqa: ARG002
        """Test if user has permission to perform action."""
        pc = self.permission_classes[0]
        pc().has_permission(request, self)
        return Response(200)

    @action(detail=False, methods=['delete'])
    def bulk_remove(self, request, *args, **kwargs):  # noqa: ARG002
        """Remove records in bulk."""
        try:
            for obj_id in list(request.data.keys()):
                self.kwargs['pk'] = obj_id
                instance = self.get_object()
                instance.delete()
            return Response(200)
        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)

    @action(detail=False, methods=['put', 'patch'])
    def bulk_edit(self, request, *args, **kwargs):  # noqa: ARG002
        """Edit records in bulk."""
        partial = request.method == 'PATCH'
        results = []
        try:
            for obj_id, props in request.data.items():
                self.kwargs['pk'] = obj_id
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=props, partial=partial)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                results.append(serializer.data)
            return Response({'data': results}, 200)
        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)

    @action(detail=False, methods=['patch'])
    def inline_update(self, request, *args, **kwargs):  # noqa: ARG002
        """Edit records inline."""
        pks = [str(pk) for pk in request.data]
        for pk in pks:
            obj = self.queryset.filter(pk=pk)
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

    def get_serializer(self, *args, **kwargs):
        """Return serializer."""
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()

        if self.options_view:
            kwargs['field_set'] = 'option'

        if self.url_view:
            kwargs['field_set'] = 'url'

        return serializer_class(*args, **kwargs)
