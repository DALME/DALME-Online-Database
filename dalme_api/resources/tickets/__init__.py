"""Interface for the dalme_api.resources.tickets module."""
from .endpoints import Tickets
from .serializers import TicketDetailSerializer, TicketSerializer

__all__ = [
    'Tickets',
    'TicketDetailSerializer',
    'TicketSerializer',
]
