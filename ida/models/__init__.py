"""Interface for the ida.models module."""
from .scoped import ScopedBase
from .tenant import Domain, Tenant
from .user import User

__all__ = [
    'Domain',
    'ScopedBase',
    'Tenant',
    'User',
]
