"""Define base functionality for API viewsets."""

from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response


class BaseViewSet(viewsets.ModelViewSet):
    """Generic viewset. Should be subclassed for specific API endpoints."""

    authentication_classes = None  # This is dynamic, see `initialize_request`.

    permission_classes = []
    oauth_permission_classes = []

    context = None
    queryset = None
    serializer_class = None

    def initialize_request(self, request, *args, **kwargs):
        """Override to switch between session or OAuth authentication systems."""
        is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

        authentication = OAuth2Authentication if is_ajax else SessionAuthentication
        self.authentication_classes = [authentication]  # Should only ever be one or the other.

        if is_ajax:
            self.permission_classes = self.oauth_permission_classes

        return super().initialize_request(request, *args, **kwargs)

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
            obj.update(**obj_data)

        return Response({'message': f'Updated {len(pks)} rows.'}, 201)

    @action(detail=True, methods=['patch'])
    def add_attribute(self, request, *args, **kwargs):  # noqa: ARG002
        """Add a new attribute to an object."""
        if not hasattr(self.get_queryset().model, 'attribute_list'):
            return Response({'error': 'This endpoint is not associated with a model with attributes.'}, 400)

        try:
            from domain.api.resources.attributes.serializers import AttributeSerializer
            from domain.models import Attribute, AttributeType

            obj = self.get_object()
            atype_ref = request.data.get('type')
            value = request.data.get('value')
            atype = (
                AttributeType.objects.get(pk=int(atype_ref))
                if atype_ref.isdigit()
                else AttributeType.objects.get(name=atype_ref)
            )
            att = Attribute(content_object=obj, attribute_type=atype, value=value)
            att.save()
            serializer = AttributeSerializer(
                Attribute.objects.get(pk=att.id)
            )  # we need to look it up to get the annotations
            return Response(serializer.data, 200)

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)

    @action(detail=True, methods=['patch'])
    def update_related(self, request, *args, **kwargs):  # noqa: ARG002
        """Update an object's related field."""
        field = request.data.get('field')
        related_id = request.data.get('value')

        if not field or not related_id:
            return Response({'error': 'A field name and a related id must be provided.'}, 400)

        try:
            obj = self.get_object()
            setattr(obj, f'{field}_id', related_id)
            obj.save()
            serializer = self.get_serializer(obj)
            return Response(serializer.data, 200)

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)

    def get_serializer_kwargs(self, **kwargs):
        """Return serializer kwargs."""
        kwargs['context'] = self.get_serializer_context()
        kwargs['action'] = self.action

        if self.options_view:
            kwargs['field_set'] = 'option'

        if self.url_view:
            kwargs['field_set'] = 'url'

        return kwargs

    def get_serializer(self, *args, **kwargs):
        """Return serializer."""
        serializer_class = self.get_serializer_class()
        kwargs = self.get_serializer_kwargs(**kwargs)

        return serializer_class(*args, **kwargs)
