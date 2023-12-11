"""Interface for the dalme_api.resources.records module."""
from .endpoints import Records
from .serializers import RecordSerializer

__all__ = [
    'RecordSerializer',
    'Records',
]
