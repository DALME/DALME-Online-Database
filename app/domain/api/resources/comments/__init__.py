"""Interface for the api.resources.comments module."""

from .endpoints import Comments
from .serializers import CommentSerializer

__all__ = [
    'Comments',
    'CommentSerializer',
]
