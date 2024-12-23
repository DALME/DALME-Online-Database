"""API endpoint for managing attributes."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from stringcase import snakecase

from django.db.models import Q

from app.access_policies import BaseAccessPolicy, GeneralAccessPolicy, WebAccessPolicy
from domain.api.viewsets import BaseViewSet
from domain.models import Attribute, AttributeType, ContentAttributes, ContentTypeExtended

from .filters import ContentTypeFilter
from .serializers import (
    AttributeSerializer,
    AttributeTypeSerializer,
    ContentAttributesSerializer,
    ContentTypeSerializer,
)


class AttributeAccessPolicy(BaseAccessPolicy):
    """Access policies for record attributes."""

    id = 'attributes-policy'


class AttributeTypesAccessPolicy(BaseAccessPolicy):
    """Access policies for attribute types."""

    id = 'attribute-types-policy'


class ContentTypes(BaseViewSet):
    """API endpoint for managing ContentTypes."""

    permission_classes = [GeneralAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & GeneralAccessPolicy]

    queryset = ContentTypeExtended.objects.all()
    serializer_class = ContentTypeSerializer
    filterset_class = ContentTypeFilter


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
                filter_kwargs = {'name': lookup_value}
                queryset = AttributeType.objects.all()
                obj = get_object_or_404(queryset, **filter_kwargs)
                self.check_object_permissions(self.request, obj)
                return obj
        return super().get_object()

    @action(detail=True, methods=['get'])
    def options(self, request, *args, **kwargs):  # noqa: ARG002
        """Return options for attribute type."""
        atype = self.get_object()
        options = atype.options.get_values(public=self.is_public)
        if options is not None:
            return Response(options, 201)
        return Response({'error': 'No options could be retrieved.'}, 400)


class WebAttributeTypes(AttributeTypes):
    """Website API endpoint for managing attribute types."""

    permission_classes = [WebAccessPolicy]
    oauth_permission_classes = [WebAccessPolicy]
    is_public = True


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

    @action(detail=False, methods=['get'])
    def options(self, request, *args, **kwargs):  # noqa: ARG002
        """Return options for list of attributes."""
        if request.GET.get('names') is not None:
            names = request.GET['names'].split(',')
            options = {}
            for name in names:
                try:
                    atype = AttributeType.objects.get(name=name)
                    options[name] = atype.options.get_values(public=self.is_public)
                except AttributeType.DoesNotExist:
                    options[name] = 'Attribute Type does not exist.'
                except AttributeError:
                    options[name] = 'No options could be retrieved.'
            if options:
                return Response(options, 201)
        return Response({'error': 'No options could be retrieved.'}, 400)


class WebAttributes(Attributes):
    """Web API endpoint for managing attributes and options."""

    permission_classes = [WebAccessPolicy]
    oauth_permission_classes = [WebAccessPolicy]
    is_public = True
