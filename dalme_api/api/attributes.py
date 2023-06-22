from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from django.apps import apps

from dalme_api.access_policies import AttributeAccessPolicy
from dalme_api.serializers import AttributeSerializer, OptionsSerializer
from dalme_app.models import Attribute, AttributeType

from .base_viewset import DALMEBaseViewSet


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
