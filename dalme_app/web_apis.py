from rest_framework import viewsets
from dalme_app.web_serializers import (RecordSerializer)
from dalme_app.models import (Source)
from rest_framework.permissions import DjangoModelPermissions
from django.db.models import Q, Count


class Records(viewsets.ModelViewSet):
    """ API endpoint for managing records for the web frontend """
    permission_classes = (DjangoModelPermissions,)
    queryset = Source.objects.filter(type=13, workflow__is_public=True).annotate(no_folios=Count('pages', filter=Q(pages__source__isnull=False)))
    serializer_class = RecordSerializer
