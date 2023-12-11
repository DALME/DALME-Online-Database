"""Interface for the dalme_api.resources.attributes module."""
from .endpoints import Attributes, AttributeTypes, ContentTypes
from .serializers import AttributeSerializer, AttributeTypeSerializer

__all__ = [
    'AttributeSerializer',
    'AttributeTypeSerializer',
    'AttributeTypes',
    'Attributes',
    'ContentTypes',
]
