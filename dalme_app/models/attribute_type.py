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
        ('RREL', 'RREL (reverse relation)'),
        ('STR', 'STR (string)'),
        ('TXT', 'TXT (text)'),
    )

    name = models.CharField(max_length=55, unique=True)
    label = models.CharField(max_length=255)
    description = models.TextField()
    data_type = models.CharField(max_length=15, choices=DATA_TYPES)
    is_local = models.BooleanField(default=False)
    source = models.CharField(max_length=255, blank=True)
    same_as = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    options = models.ForeignKey('OptionsList', on_delete=models.SET_NULL, null=True)

    class Meta:  # noqa: D106
        ordering = ['id']

    def __str__(self):  # noqa: D105
        return self.name

    def get_options(self):
        """Return options for attribute type."""
        return self.options
