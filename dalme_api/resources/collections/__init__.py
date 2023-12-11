"""Interface for the dalme_api.resources.collections module."""
from .endpoints import Collections
from .serializers import CollectionSerializer

__all__ = [
    'Collections',
    'CollectionSerializer',
]
