"""Interface for the domain.models.permission module.

Includes definitions of fields, models, and managers.

"""

from .permission import PERMISSION_TYPES, Permission
from .permission_mixin import PermissionMixin

__all__ = [
    'PERMISSION_TYPES',
    'Permission',
    'PermissionMixin',
]
