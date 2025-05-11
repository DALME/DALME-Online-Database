"""API endpoint for managing attributes."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from stringcase import snakecase

from django.db.models import Q

from app.access_policies import BaseAccessPolicy, WebAccessPolicy
from domain.api.resources.content_types.serializers import ContentAttributesSerializer
from domain.api.viewsets import BaseViewSet
from domain.models import Attribute, AttributeType, ContentAttributes

from .serializers import (
    AttributeSerializer,
    AttributeTypeSerializer,
)


class AttributeAccessPolicy(BaseAccessPolicy):
    """Access policies for record attributes."""

    id = 'attributes-policy'


class AttributeTypesAccessPolicy(BaseAccessPolicy):
    """Access policies for attribute types."""

    id = 'attribute-types-policy'


class AttributeTypes(BaseViewSet):
    """API endpoint for managing attribute types."""

    permission_classes = [AttributeTypesAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & AttributeTypesAccessPolicy]
    queryset = AttributeType.objects.all()
    serializer_class = AttributeTypeSerializer
    is_public = False

    def get_queryset(self, *args, **kwargs):
        """Return filtered querysets."""
        if self.request.GET.get('short_names') is not None:
            q_short_names = self.request.GET.get('short_names')
            q_short_names = [snakecase(short_name) for short_name in q_short_names.split(',')]
            return AttributeType.objects.filter(name__in=q_short_names)

        if self.request.GET.get('filter') is not None:
            filter_v = self.request.GET['filter'].split(',')
            filter_q = Q(**{filter_v[0]: filter_v[1]})
            return ContentAttributes.objects.filter(filter_q)

        return super().get_queryset(*args, **kwargs)

    def get_serializer_class(self):
        """Return serializer class."""
        if self.request.GET.get('filter') is not None and self.request.GET['filter'].split(',')[0] == 'content_type':
            return ContentAttributesSerializer
        return super().get_serializer_class()

    def get_object(self):
        """Return the object the view is displaying when requested by either id or name."""
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg in self.kwargs:
            lookup_value = self.kwargs[lookup_url_kwarg]
            if not str(lookup_value).isdigit():
                # check if provided name is likely to be an internal name for a related field
                # and add the name minus the '_id' or '_ids' suffix to the filter
                if lookup_value.endswith(('_id', '_ids')):
                    filter_args = Q(name=lookup_value) | Q(name='_'.join(lookup_value.split('_')[:-1]))
                else:
                    filter_args = Q(name=lookup_value)

                queryset = AttributeType.objects.all()
                obj = get_object_or_404(queryset, filter_args)
                self.check_object_permissions(self.request, obj)
                return obj
        return super().get_object()

    @action(detail=True, methods=['get'])
    def opts(self, request, *args, **kwargs):  # noqa: ARG002
        """Return options for single attribute type."""
        serialize = request.GET.get('serialize', False)
        model = request.GET.get('model', None)
        filters = request.GET.get('filters', None)
        content = request.GET.get('content', None)
        atype = self.get_object()

        try:
            options_obj = atype.get_options_for_content(content)
            options = options_obj.get_values(
                public=self.is_public,
                model=model,
                filters=filters,
                serialize=serialize,
            )

        except AttributeError:
            options = None

        if options:
            return Response(options, 200)

        return Response({'error': 'No options could be retrieved.'}, 400)

    @action(detail=False, methods=['get'])
    def options(self, request, *args, **kwargs):  # noqa: ARG002
        """Return options for a list of attribute types."""
        if request.GET.get('names') is None:
            return Response({'error': 'No list of attributes was provided.'}, 400)

        serialize = request.GET.get('serialize', False)
        names = request.GET['names'].split(',')
        options = {}
        for name in names:
            try:
                atype = AttributeType.objects.get(name=name)
                options[name] = atype.options.get_values(public=self.is_public, serialize=serialize)
            except AttributeType.DoesNotExist:
                options[name] = 'Attribute Type does not exist.'
            except AttributeError:
                options[name] = 'No options could be retrieved.'

        if options:
            return Response(options, 200)

        return Response({'error': 'No options could be retrieved.'}, 400)


class Attributes(BaseViewSet):
    """API endpoint for managing attributes and options."""

    permission_classes = [AttributeAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & AttributeAccessPolicy]
    queryset = Attribute.objects.all().order_by('attribute_type')
    serializer_class = AttributeSerializer
    is_public = False

    def get_object(self):
        """Return the object the view is displaying."""
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg in self.kwargs and str(self.kwargs[lookup_url_kwarg]).isdigit():
            lookup_value = self.kwargs[lookup_url_kwarg]
            filter_kwargs = {self.lookup_field: lookup_value}
            queryset = AttributeType.objects.all()
            obj = get_object_or_404(queryset, **filter_kwargs)
            self.check_object_permissions(self.request, obj)
            return obj
        return super().get_object()

    @action(detail=True, methods=['get', 'post'])
    def options(self, request, *args, **kwargs):  # noqa: ARG002
        """Return options for attribute."""
        serialize = request.GET.get('serialize', False)
        model = request.GET.get('model', None)
        filters = request.GET.get('filters', None)
        attr = self.get_object()

        try:
            options_obj = attr.get_options()
            options = options_obj.get_values(
                public=self.is_public,
                model=model,
                filters=filters,
                serialize=serialize,
            )
        except AttributeError:
            options = None

        if options:
            return Response(options, 200)

        return Response({'error': 'No options could be retrieved.'}, 400)


class WebAttributeTypes(AttributeTypes):
    """Website API endpoint for managing attribute types."""

    permission_classes = [WebAccessPolicy]
    oauth_permission_classes = [WebAccessPolicy]
    is_public = True


class WebAttributes(Attributes):
    """Web API endpoint for managing attributes and options."""

    permission_classes = [WebAccessPolicy]
    oauth_permission_classes = [WebAccessPolicy]
    is_public = True
