"""Interface for the api.resources.pages module."""

from .endpoints import Pages
from .serializers import PageSerializer

__all__ = [
    'PageSerializer',
    'Pages',
]
