"""Interface for the ida.models.utils module.

Includes mixins used to more easily associate common data points
with system data models as well as other reusable utilities.

"""

from .attestation_mixin import AttestationMixin
from .attribute_field import AttributeField
from .attribute_mixin import AttributeMixin
from .comment_mixin import CommentMixin
from .historical_date import HistoricalDate
from .owned_mixin import OwnedMixin
from .permissions_mixin import PermissionsMixin
from .relationship_mixin import RelationshipMixin
from .tagging_mixin import TaggingMixin
from .tenant_scoped_mixin import ScopedBase
from .tracking_mixin import TrackingMixin
from .uuid_mixin import UuidMixin

BASE_DATA_TYPES = (
    ('BOOL', 'BOOL (boolean)'),
    ('INT', 'INT (integer)'),
    ('JSON', 'JSON (data)'),
    ('STR', 'STR (string)'),
)

DATA_TYPES = sorted(
    [
        *BASE_DATA_TYPES,
        ('DATE', 'DATE (date)'),
        ('FKEY', 'FKEY (foreign key)'),
        ('FLOAT', 'FLOAT (floating point)'),
        ('RREL', 'RREL (reverse relation)'),
    ],
    key=lambda x: x[0],
)


__all__ = [
    'AttestationMixin',
    'AttributeField',
    'AttributeMixin',
    'BASE_DATA_TYPES',
    'CommentMixin',
    'DATA_TYPES',
    'HistoricalDate',
    'OwnedMixin',
    'PermissionsMixin',
    'RelationshipMixin',
    'ScopedBase',
    'TaggingMixin',
    'TrackingMixin',
    'UuidMixin',
]
