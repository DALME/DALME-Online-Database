"""API endpoint for managing issue tickets."""
from datetime import datetime

from rest_framework.decorators import action
from rest_framework.response import Response

from django.utils import timezone

from dalme_api.access_policies import BaseAccessPolicy
from dalme_api.base_viewset import DALMEBaseViewSet
from dalme_api.filters import TicketFilter
from dalme_app.models import Ticket

from .serializers import TicketSerializer


class TicketAccessPolicy(BaseAccessPolicy):
    """Access policies for Tickets endpoint."""

    id = 'tickets-policy'  # noqa: A003


class Tickets(DALMEBaseViewSet):
    """API endpoint for managing issue tickets."""

    permission_classes = (TicketAccessPolicy,)
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filterset_class = TicketFilter
    search_fields = ['subject', 'description']
    ordering_fields = ['id', 'subject', 'description', 'status', 'creation_user', 'creation_timestamp', 'assigned_to']
    ordering = ['status', 'id']

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

            return Response({'username': self.request.user.username}, 201)

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)
