"""Interface for the domain.models.tag module.

Includes definitions of fields, models, and managers.

"""

from .tag import Tag
from .tag_mixin import TagMixin

__all__ = [
    'Tag',
    'TagMixin',
]
