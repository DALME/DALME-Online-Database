"""AttributeField definition."""

import contextlib
import json

from django.apps import apps
from django.db import models
from django.db.models.fields.json import JSONExact, KeyTransform, KeyTransformExact

from .historical_date import HistoricalDate


class AttributeField(models.JSONField):
    def from_db_value(self, value, expression, connection):
        value = super().from_db_value(value, expression, connection)

        if value is None:
            return value

        match value['dtype']:
            case 'DATE':
                return HistoricalDate(value['value'])
            case 'FKEY':
                return self.value_to_instance(value['value'])
            case 'INT':
                return int(value['value'])
            case 'FLOAT':
                return float(value['value'])
            case _:
                return value['value']

    def to_python(self, value, dtype=None, include_dtype=False):
        if value is None:
            return value

        if isinstance(value, str):
            with contextlib.suppress(json.JSONDecodeError):
                json_value = json.loads(value)
                dtype = json_value.get('dtype')
                value = json_value.get('value')

        if not dtype:
            dtype = self.get_dtype(value)

        if include_dtype:
            return self.get_value_by_type(value, dtype), dtype

        return self.get_value_by_type(value, dtype)

    def get_value_by_type(self, value, dtype):
        match dtype:
            case 'DATE':
                return HistoricalDate(value)
            case 'FKEY':
                return self.value_to_instance(value)
            case 'INT':
                return int(value)
            case 'FLOAT':
                return float(value)
            case _:
                return value

    def value_to_instance(self, value):
        if isinstance(value, models.Model):
            return value
        try:
            model = apps.get_model(app_label=value['app'], model_name=value['model'])
            return model.objects.get(pk=value['id'])
        except (KeyError, TypeError) as e:
            raise ValueError from e

    def instance_to_value(self, instance):
        return {
            'app': instance._meta.app_label,  # noqa: SLF001
            'model': instance._meta.model.__name__.lower(),  # noqa: SLF001
            'id': str(instance.pk),
        }

    def get_dtype(self, value):
        if isinstance(value, models.Model):
            return 'FKEY'
        if isinstance(value, (list | tuple | dict)):
            return 'JSON'
        if isinstance(value, HistoricalDate):
            return 'DATE'
        return type(value).__name__.upper()

    def get_prep_value(self, value):
        """Perform preliminary non-db specific value checks and conversions."""
        value = super().get_prep_value(value)
        return self.to_python(value)

    def get_db_prep_save(self, value, connection):
        if value is None:
            return value

        value, dtype = self.to_python(value, include_dtype=True)
        rep = {'dtype': dtype}

        if dtype == 'FKEY':
            rep['value'] = self.instance_to_value(value)
        elif dtype == 'DATE':
            rep['value'] = value.serialize()
        else:
            rep['value'] = value

        return connection.ops.adapt_json_value(rep, self.encoder)


class AttributeExact(JSONExact):
    def process_lhs(self, compiler, connection, lhs=None):
        if self.lhs and not isinstance(self.lhs, AttributeKeyTransform):
            self.lhs = AttributeKeyTransform('value', self.lhs)
        lhs_sql, params = super().process_lhs(compiler, connection, lhs)
        return lhs_sql, list(params)


AttributeField.register_lookup(AttributeExact)


class AttributeKeyTransform(KeyTransform):
    def preprocess_lhs(self, compiler, connection):
        key_transforms = [self.key_name]
        previous = self.lhs
        while isinstance(previous, KeyTransform):
            key_transforms.insert(0, previous.key_name)
            previous = previous.lhs
        lhs, params = compiler.compile(previous)
        if connection.vendor == 'oracle':
            key_transforms = [key.replace('%', '%%') for key in key_transforms]
        # if needed, inject 'value'
        if key_transforms[0] != 'value':
            key_transforms.insert(0, 'value')
        return lhs, params, key_transforms


class KeyTransformExact(KeyTransformExact, AttributeExact):
    def __init__(self, key_transform, *args, **kwargs):
        if not isinstance(key_transform, KeyTransform):
            msg = 'Transform should be an instance of KeyTransform in order to use this lookup.'
            raise TypeError(msg)
        key_text_transform = AttributeKeyTransform(
            key_transform.key_name,
            *key_transform.source_expressions,
            **key_transform.extra,
        )
        super().__init__(key_text_transform, *args, **kwargs)


KeyTransform.register_lookup(KeyTransformExact)
