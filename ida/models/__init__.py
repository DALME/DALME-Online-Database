"""Interface for the ida.models module."""
from .agent import Agent, Organization, Person
from .concept import Concept
from .group import GroupProperties
from .headword import Headword
from .tenant import Domain, Tenant
from .ticket import Ticket
from .token import Token
from .transcription import Transcription
from .user import User
from .wordform import Wordform

__all__ = [
    'Agent',
    'Concept',
    'Domain',
    'GroupProperties',
    'Headword',
    'Organization',
    'Person',
    'Tenant',
    'Ticket',
    'Token',
    'Transcription',
    'User',
    'Wordform',
]
