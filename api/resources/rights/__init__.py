"""Interface for the api.resources.rights module."""

from .endpoints import Rights
from .serializers import RightsPolicySerializer

__all__ = [
    'Rights',
    'RightsPolicySerializer',
]
