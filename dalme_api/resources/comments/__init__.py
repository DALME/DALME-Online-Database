"""Interface for the dalme_api.resources.comments module."""
from .endpoints import Comments
from .serializers import CommentSerializer

__all__ = [
    'Comments',
    'CommentSerializer',
]
