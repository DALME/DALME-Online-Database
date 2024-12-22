"""Interface for the api.resources.records module."""

from .endpoints import PURLEndpoint, Records, WebRecords
from .serializers import RecordSerializer, RecordTypeSerializer

__all__ = [
    'PURLEndpoint',
    'RecordSerializer',
    'Records',
    'RecordTypeSerializer',
    'WebRecords',
]
