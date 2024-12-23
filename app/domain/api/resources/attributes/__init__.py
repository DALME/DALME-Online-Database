"""Interface for the api.resources.attributes module."""

from .endpoints import Attributes, AttributeTypes, ContentTypes, WebAttributes, WebAttributeTypes
from .serializers import AttributeSerializer, AttributeTypeSerializer

__all__ = [
    'AttributeSerializer',
    'AttributeTypeSerializer',
    'AttributeTypes',
    'Attributes',
    'ContentTypes',
    'WebAttributeTypes',
    'WebAttributes',
]
