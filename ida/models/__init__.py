"""Interface for the ida.models module."""
from .scoped import ScopedBase
from .tenant import Domain, Tenant

__all__ = [
    'Domain',
    'ScopedBase',
    'Tenant',
]
