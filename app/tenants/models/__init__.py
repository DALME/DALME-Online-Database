"""Interface for the tenants.models module.

Includes definitions of fields, models, and managers.

"""

from .tenant import Domain, Tenant
from .tenant_mixin import TenantMixin

__all__ = [
    'Domain',
    'Tenant',
    'TenantMixin',
]
