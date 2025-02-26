"""ListField definition."""

from django.apps import apps
from django.contrib.postgres.fields import ArrayField


class ListField(ArrayField):
    """Field that stores both arrays and single instances.

    An extension of the PostGREs-specific ArrayField that returns either
    a list of instances or a single instance depending on its member count.

    ListField only supports PostGREs database engine.
    """

    def __init__(self, base_field, size=None, is_unique=True, **kwargs):
        self.is_unique = is_unique
        super().__init__(base_field, size=size, **kwargs)

    def get_db_prep_value(self, value, connection, prepared=False):  # noqa: ARG002
        if isinstance(value, list | tuple):
            return [self.base_field.get_db_prep_value(i, connection, prepared=False) for i in value]
        if isinstance(value, self.base_field):
            return [self.base_field.get_db_prep_value(value, connection, prepared=False)]
        return value

    def _from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return [self.base_field.from_db_value(item, expression, connection) for item in value]

    @property
    def model(self):
        return apps.get_model(app_label='domain', model_name='attribute')
