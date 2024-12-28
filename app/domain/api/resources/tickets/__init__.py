"""Interface for the api.resources.tickets module."""

from .endpoints import Tickets
from .serializers import TicketDetailSerializer, TicketSerializer

__all__ = [
    'TicketDetailSerializer',
    'TicketSerializer',
    'Tickets',
]
