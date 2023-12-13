"""Interface for the ida.models module."""
from .agent import Agent, Organization, Person
from .concept import Concept
from .group import GroupProperties
from .headword import Headword
from .tenant import Domain, Tenant
from .user import User

__all__ = [
    'Agent',
    'Concept',
    'Domain',
    'GroupProperties',
    'Headword',
    'Organization',
    'Person',
    'Tenant',
    'User',
]
