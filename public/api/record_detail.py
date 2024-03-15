"""API endpoint for single record instances."""

from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ida.models import Record
from public.serializers import RecordSerializer


class RecordDetail(RetrieveAPIView):
    """API endpoint for single record instances."""

    model = Record
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    lookup_url_kwarg = 'pk'
    permission_classes = [IsAuthenticatedOrReadOnly]
