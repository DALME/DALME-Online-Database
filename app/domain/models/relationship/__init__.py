"""Interface for the domain.models.relationship module.

Includes definitions of fields, models, and managers.

"""

from .relationship import Relationship, RelationshipType
from .relationship_mixin import RelationshipMixin

__all__ = [
    'Relationship',
    'RelationshipMixin',
    'RelationshipType',
]
