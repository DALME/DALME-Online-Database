from rest_framework import viewsets
from dalme_app.web_serializers import (RecordSerializer, CollectionSerializer)
from dalme_app.models import (Source, Set)
from rest_framework.permissions import DjangoModelPermissions
from django.db.models import Q, Count
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class Records(viewsets.ModelViewSet):
    """ API endpoint for managing records for the web frontend """
    permission_classes = (DjangoModelPermissions,)
    queryset = Source.objects.filter(type=13, workflow__is_public=True).annotate(no_folios=Count('pages', filter=Q(pages__source__isnull=False)))
    serializer_class = RecordSerializer


class Collections(viewsets.ModelViewSet):
    """ API endpoint for managing collections on the web frontend """
    permission_classes = (DjangoModelPermissions,)
    queryset = Set.objects.filter(set_type=2, is_public=True)
    serializer_class = CollectionSerializer

    @action(detail=True, methods=['post', 'get'])
    def get_stats(self, request, *args, **kwargs):
        result = {}
        object = get_object_or_404(self.queryset, pk=kwargs.get('pk'))
        try:
            data = []
            # count of inventories
            # count of objects
            # languages represented [full name + abbv]
            # temporal coverage
            # status groups represented
            data.append({
                'label': 'Inventories',
                'type': 'bar',
                'data': object.get_public_member_count
            })
            data.append({
                'label': 'Language(s)',
                'type': 'pill',
                'data': object.get_public_languages
            })
            data.append({
                'label': 'Coverage',
                'type': 'histogram',
                'data': object.get_public_time_coverage
            })
            data.append({
                'label': object.stat_title,
                'type': 'text',
                'data': object.stat_text
            })
            result['data'] = data
            status = 201
        except Exception as e:
            result['error'] = str(e)
            status = 400
        return Response(result, status)
