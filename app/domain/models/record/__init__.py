"""Interface for the domain.models.record module.

Includes definitions of fields, models, and managers.

"""

from .record import PageNode, Record, RecordGroup, RecordType
from .record_helpers import format_credit_line, format_credits, format_source

__all__ = [
    'format_credit_line',
    'format_credits',
    'format_source',
    'PageNode',
    'RecordGroup',
    'Record',
    'RecordType',
]
