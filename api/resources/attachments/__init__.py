"""Interface for the api.resources.attachments module."""

from .endpoints import Attachments
from .serializers import AttachmentSerializer

__all__ = [
    'AttachmentSerializer',
    'Attachments',
]
