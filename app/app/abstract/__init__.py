"""Interface for the app.abstract module.

Includes mixins used to more easily associate common data points with system data models.
None of the models defined here should map to a database table.
They should all be abstract or proxy models.

"""

from .custom_manager import CustomManager, CustomQuerySet
from .owned_mixin import OwnedMixin
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
    'BASE_DATA_TYPES',
    'DATA_TYPES',
    'CustomManager',
    'CustomQuerySet',
    'OwnedMixin',
    'TrackingMixin',
    'UuidMixin',
]
