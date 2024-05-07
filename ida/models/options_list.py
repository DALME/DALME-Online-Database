"""Options-related models."""

from django.db import models
from django.db.models import options

from ida.models.templates import IDABasic, IDAIntid
from ida.models.tenant_scoped import ScopedBase

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class OptionsList(IDAIntid):
    """Stores lists of attribute value options. Payload format as follows.

    `db_records`: {
        'app': FOO,
        'model': BAR,
        'filters': {'is_active': True}, # queryset filters as dict, optional
        'concordance': {'label': FOO.BAR, 'value': BAZ, 'group': BAY, # optional 'detail': BAX, # optional},
    }
    `field_choices`: {
        'app': FOO,
        'model': BAR,
        'choices': BAZ
    }
    `static_list`: [
        {'label': FOO, 'value': BAR, 'group': BAZ, # optional 'detail': BAY, # optional},
        ...
    ]
    """

    PAYLOAD_TYPES = (
        ('db_records', 'DB Records'),
        ('field_choices', 'Field Choices'),
        ('static_list', 'Static List'),
    )

    name = models.CharField(max_length=255)
    payload_type = models.CharField(max_length=15, choices=PAYLOAD_TYPES)
    description = models.TextField()


class OptionsValue(ScopedBase, IDABasic):
    """Stores tenanted static lists of values."""

    op_list = models.ForeignKey(OptionsList, on_delete=models.CASCADE, related_name='values')
    payload = models.JSONField()
