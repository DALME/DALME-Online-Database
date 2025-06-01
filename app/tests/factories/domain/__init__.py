"""Interface for the tests.factories.domain module."""

from .agents import OrganizationFactory, PersonFactory
from .records import RecordFactory

__all__ = [
    'OrganizationFactory',
    'PersonFactory',
    'RecordFactory',
]
