"""Interface for the dalme_api.resources.groups module."""
from .endpoints import Groups
from .serializers import GroupSerializer

__all__ = [
    'GroupSerializer',
    'Groups',
]
