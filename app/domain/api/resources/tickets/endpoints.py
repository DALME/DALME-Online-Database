"""API endpoint for managing issue tickets."""

from datetime import datetime

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from django.utils import timezone

from app.access_policies import BaseAccessPolicy
from domain.api.viewsets import BaseViewSet
from domain.models import Ticket

from .filters import TicketFilter
from .serializers import TicketSerializer


class TicketAccessPolicy(BaseAccessPolicy):
    """Access policies for Tickets endpoint."""

    id = 'tickets-policy'


class Tickets(BaseViewSet):
    """API endpoint for managing issue tickets."""

    permission_classes = [TicketAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & TicketAccessPolicy]

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filterset_class = TicketFilter
    search_fields = ['subject', 'description']
    ordering_fields = ['id', 'subject', 'description', 'status', 'creation_user', 'creation_timestamp', 'assigned_to']
    ordering = ['status', 'id']

    def get_object(self):
        """Return the object the view is displaying when requested by either id or number."""
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg in self.kwargs:
            lookup_value = self.kwargs[lookup_url_kwarg]
            if str(lookup_value).isdigit():
                filter_kwargs = {'number': lookup_value}
                obj = get_object_or_404(self.get_queryset(), **filter_kwargs)
                self.check_object_permissions(self.request, obj)
                return obj
        return super().get_object()

    @action(detail=True, methods=['patch'])
    def set_state(self, request, *args, **kwargs):  # noqa: ARG002
        """Set ticket state."""
        obj = self.get_object()
        action = self.request.data.get('action')
        if action is None:
            return Response({'error': 'Request must include an action.'}, 400)

        if action not in ['Open', 'Close']:
            return Response({'error': f'"{action}" is not a valid action.'}, 400)

        try:
            if action == 'Close':
                obj.status = 1
                obj.closing_user = self.request.user
                obj.closing_date = datetime.now(
                    tz=timezone.get_current_timezone(),
                ).date()
                obj.save(
                    update_fields=[
                        'status',
                        'modification_user',
                        'modification_timestamp',
                        'closing_user',
                        'closing_date',
                    ],
                )
            elif action == 'Open':
                obj.status = 0
                obj.save(update_fields=['status', 'modification_user', 'modification_timestamp'])

            return Response({'username': self.request.user.username}, 200)

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)
