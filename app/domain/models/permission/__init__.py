"""Interface for the domain.models.permission module.

Includes definitions of fields, models, and managers.

"""

from .permission import Permission
from .permission_mixin import PermissionMixin

__all__ = [
    'Permission',
    'PermissionMixin',
]
