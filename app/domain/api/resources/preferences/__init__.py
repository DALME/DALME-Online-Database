"""Interface for the api.resources.preferences module."""

from .endpoints import Preferences
from .serializers import PreferenceSerializer

__all__ = [
    'PreferenceSerializer',
    'Preferences',
]
