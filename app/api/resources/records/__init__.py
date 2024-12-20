"""Interface for the api.resources.records module."""

from .endpoints import Records, WebRecords
from .serializers import RecordSerializer, RecordTypeSerializer

__all__ = [
    'RecordSerializer',
    'Records',
    'RecordTypeSerializer',
    'WebRecords',
]
