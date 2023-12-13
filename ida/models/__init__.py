"""Interface for the ida.models module."""
from .group import GroupProperties
from .scoped import ScopedBase
from .tenant import Domain, Tenant
from .user import User

__all__ = [
    'Domain',
    'GroupProperties',
    'ScopedBase',
    'Tenant',
    'User',
]
