"""Interface for the domain.models.attribute module.

Includes definitions of fields, models, and managers.

"""

from .comment import Comment
from .comment_mixin import CommentMixin

__all__ = [
    'Comment',
    'CommentMixin',
]
