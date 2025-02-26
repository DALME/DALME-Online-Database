"""Interface for the api.resources.records module."""

from .endpoints import RecordGroups
from .serializers import RecordGroupSerializer

__all__ = [
    'RecordGroupSerializer',
    'RecordGroups',
]
