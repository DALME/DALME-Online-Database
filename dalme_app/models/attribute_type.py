from django.db import models

from dalme_app.models.templates import dalmeIntid


class AttributeType(dalmeIntid):
    """Stores attribute definitions."""

    DATA_TYPES = (
        ('BOOL', 'BOOL (boolean)'),
        ('DATE', 'DATE (date)'),
        ('DEC', 'DEC (decimal)'),
        ('FKEY', 'FKEY (foreign key)'),
        ('INT', 'INT (integer)'),
        ('JSON', 'JSON (data)'),
        ('STR', 'STR (string)'),
        ('TXT', 'TXT (text)'),
        ('FK-UUID', 'FK-UUID (DALME record)'),
        ('FK-INT', 'FK-INT (DALME record)'),
    )

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55, unique=True)
    description = models.TextField()
    data_type = models.CharField(max_length=15, choices=DATA_TYPES)
    source = models.CharField(max_length=255, blank=True)
    same_as = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        db_column='same_as',
    )
    options_list = models.CharField(max_length=255, blank=True)
    options_source = models.JSONField(null=True)

    class Meta:  # noqa: D106
        ordering = ['id']

    def __str__(self):  # noqa: D105
        return self.name
