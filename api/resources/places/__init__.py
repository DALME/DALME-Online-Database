"""Interface for the api.resources.places module."""

from .endpoints import Places
from .serializers import PlaceSerializer

__all__ = [
    'Places',
    'PlaceSerializer',
]
