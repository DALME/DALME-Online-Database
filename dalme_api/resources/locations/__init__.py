"""Interface for the dalme_api.resources.locations module."""
from .endpoints import Locations
from .serializers import LocationSerializer

__all__ = [
    'LocationSerializer',
    'Locations',
]
