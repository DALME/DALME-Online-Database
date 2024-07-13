"""Interface for the ida.models.entity module.

Includes definitions of fields, models, and managers.

"""

from .attestation_mixin import AttestationMixin
from .entity_phrase import EntityPhrase

__all__ = [
    'AttestationMixin',
    'EntityPhrase',
]
