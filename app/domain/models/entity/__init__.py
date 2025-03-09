"""Interface for the domain.models.entity module.

Includes definitions of fields, models, and managers.

"""

from .attestation_mixin import AttestationMixin
from .entity_phrase import EntityPhrase

__all__ = [
    'AttestationMixin',
    'EntityPhrase',
]
