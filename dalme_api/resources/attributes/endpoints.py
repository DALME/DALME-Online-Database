"""API endpoint for managing attributes."""
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from stringcase import snakecase

from django.apps import apps
from django.db.models import Q

from dalme_api.access_policies import BaseAccessPolicy, GeneralAccessPolicy
from dalme_api.base_viewset import DALMEBaseViewSet
from dalme_api.filters import ContentTypeFilter
from dalme_app.models import Attribute, AttributeType
from ida.models import ContentAttributes, ContentTypeExtended

from .serializers import (
    AttributeSerializer,
    AttributeTypeSerializer,
    ContentAttributesSerializer,
    ContentTypeSerializer,
)


class AttributeAccessPolicy(BaseAccessPolicy):
    """Access policies for record attributes."""

    id = 'attributes-policy'  # noqa: A003


class ContentTypes(DALMEBaseViewSet):
    """API endpoint for managing ContentTypes."""

    permission_classes = (GeneralAccessPolicy,)
    queryset = ContentTypeExtended.objects.all()
    serializer_class = ContentTypeSerializer
    filterset_class = ContentTypeFilter


class OptionsSerializer(serializers.Serializer):
    """Serializer for UI options."""

    label = serializers.CharField()
    value = serializers.CharField()
    group = serializers.CharField(required=False)
    detail = serializers.CharField(required=False)

    class Meta:
        fields = ['label', 'value', 'group', 'detail']

    def __init__(self, *args, **kwargs):
        self.concordance = kwargs.pop('concordance', None)
        super().__init__(*args, **kwargs)

    def get_fields(self):
        """Alter fields based on concordance."""
        fields = super().get_fields()
        if self.concordance:
            for key, value in self.concordance.items():
                fields[key] = serializers.CharField(source=value)
        return fields


class AttributeTypes(DALMEBaseViewSet):
    """API endpoint for managing attribute types."""

    permission_classes = (GeneralAccessPolicy,)
    queryset = AttributeType.objects.all()
    serializer_class = AttributeTypeSerializer

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


class Attributes(DALMEBaseViewSet):
    """API endpoint for managing attributes and options."""

    permission_classes = (AttributeAccessPolicy,)
    queryset = Attribute.objects.all().order_by('attribute_type')
    serializer_class = AttributeSerializer

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

    @action(detail=True, methods=['get'])
    def options(self, request, *args, **kwargs):  # noqa: ARG002
        """Return options for attribute."""
        options = self.get_options(self.get_object())
        if options is not None:
            return Response(options, 201)
        return Response({'error': 'No options could be retrieved.'}, 400)

    @staticmethod
    def get_options(attribute):
        """Return list of options for an attribute."""
        options = attribute.get_options()
        try:
            if options.type == 'db_records':
                model = apps.get_model(options.payload.get('app'), options.payload.get('model'))
                filters = options.payload.get('filters')
                queryset = model.objects.filter(**filters) if filters else model.objects.all()
                serializer = OptionsSerializer(queryset, many=True, concordance=options.payload.get('concordance'))
                return serializer.data

            if options.type == 'field_choices':
                model = apps.get_model(options.payload.get('app'), options.payload.get('model'))
                choices = getattr(model, options.payload.get('choices'))
                data = [{'label': i[1], 'value': i[0]} for i in choices]
                serializer = OptionsSerializer(data, many=True)
                return serializer.data

            if options.type == 'static_list':
                serializer = OptionsSerializer(options.payload, many=True)
                return serializer.data

        except AttributeError:
            return None