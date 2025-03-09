"""Interface for the api.resources.collections module."""

from .endpoints import Collections
from .serializers import CollectionSerializer

__all__ = [
    'CollectionSerializer',
    'Collections',
]
