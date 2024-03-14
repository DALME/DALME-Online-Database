"""Interface for the api.resources.transcriptions module."""

from .endpoints import Transcriptions
from .serializers import TranscriptionSerializer

__all__ = [
    'TranscriptionSerializer',
    'Transcriptions',
]
