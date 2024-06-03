"""AttributeField definition."""

import contextlib
import json

from django import forms
from django.apps import apps
from django.core import exceptions
from django.db import models
from django.db.models import Field, expressions, lookups
from django.db.models.fields.json import (
    CaseInsensitiveMixin,
    ContainedBy,
    DataContains,
    HasAnyKeys,
    HasKey,
    HasKeyLookup,
    HasKeyOrArrayIndex,
    HasKeys,
    KeyTextTransform,
    KeyTransform,
    KeyTransformFactory,
    KeyTransformNumericLookupMixin,
    KeyTransformTextLookupMixin,
    compile_json_path,
)
from django.db.models.fields.mixins import CheckFieldDefaultMixin

from .historical_date import HistoricalDate


class AttributeField(CheckFieldDefaultMixin, Field):
    """Field to store attributes as JSON-encoded data.

    The field type is based on the default JSONField class,
    but doesn't subclass it to avoid interfering with the key
    transform mechanics.

    AttributeField only supports PostGREs database engine.
    """

    empty_strings_allowed = False
    description = 'An attribute'
    default_error_messages = {'invalid': 'Value must be JSON-serializable.'}
    _default_hint = ('dict', '{}')

    def from_db_value(self, value, expression, connection):  # noqa: ARG002
        """Convert data when loaded from the database."""
        if value is None:
            return value

        with contextlib.suppress(json.JSONDecodeError):
            value = json.loads(value)

        if isinstance(expression, AFKeyTransform):
            return value

        if value.get('dtype'):
            value = self.get_value_by_type(value.get('value'), value['dtype'])

        return value

    def get_internal_type(self):
        return 'JSONField'

    def get_prep_value(self, value):
        """Perform preliminary non-db specific value checks and conversions."""
        value = super().get_prep_value(value)
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        """Return field's value prepared for interacting with the database backend."""
        if not prepared:
            value = self.get_prep_value(value)

        if isinstance(value, expressions.Value) and isinstance(value.output_field, AttributeField):
            value = value.value
        elif hasattr(value, 'as_sql'):
            return value

        return connection.ops.adapt_json_value(value, None)

    def get_db_prep_save(self, value, connection):
        """Return field's value prepared for saving into a database."""
        if value is None:
            return value

        value, dtype = self.to_python(value, include_dtype=True)

        return connection.ops.adapt_json_value(
            {
                'dtype': dtype,
                'value': self.instance_to_value(value) if dtype == 'FKEY' else value,
            },
            None,
        )

    def get_transform(self, name):
        transform = super().get_transform(name)
        if transform:
            return transform
        return AFKeyTransformFactory(name)

    def validate(self, value, model_instance):
        """Validate value and raise ValidationError if necessary."""
        super().validate(value, model_instance)
        try:
            json.dumps(value)
        except TypeError as e:
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            ) from e

    def value_to_string(self, obj):
        """Return a string value of this field from the passed obj (used by the serialization framework)."""
        return str(self.value_from_object(obj))

    def formfield(self, **kwargs):
        """Return a django.forms.Field instance for this field."""
        return super().formfield(**{'form_class': forms.JSONField, **kwargs})

    def to_python(self, value, dtype=None, include_dtype=False):
        """Convert input value into Python data type."""
        if value is None:
            return value

        if isinstance(value, str):
            with contextlib.suppress(json.JSONDecodeError, AttributeError):
                json_value = json.loads(value)
                dtype = json_value.get('dtype')
                value = json_value.get('value')

        if not dtype:
            dtype = self.get_dtype(value)

        if include_dtype:
            return self.get_value_by_type(value, dtype), dtype
        return self.get_value_by_type(value, dtype)

    def get_value_by_type(self, value, dtype):
        """Return value based on its data type."""
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
        """Return a model instance from a JSON-serializable dict."""
        if isinstance(value, models.Model):
            return value
        app = value.get('app')
        model = value.get('model')
        obj_id = value.get('id')
        if app and model and obj_id:
            try:
                model = apps.get_model(app_label=app, model_name=model)
                return model.objects.get(pk=obj_id)
            except model.DoesNotExist:
                return value
        return value

    def instance_to_value(self, instance):
        """Return a JSON-serializable dict representing a model instance.

        By default the dict will include the app label ('app'), 'model', and
        the instance 'id'. In addition, if the attribute 'attribute_matching_fields'
        is set in the model's Meta class, the values for the listed fields will also
        be included, and therefore made available for lookups when querying the
        serialized representation of the instance.
        """
        value = {
            'app': instance._meta.app_label,  # noqa: SLF001
            'model': instance._meta.model.__name__.lower(),  # noqa: SLF001
            'id': str(instance.pk),
        }

        if hasattr(instance._meta, 'attribute_matching_fields'):  # noqa: SLF001
            for field in instance._meta.attribute_matching_fields:  # noqa: SLF001
                value[field] = str(getattr(instance, field, None))

        return value

    def get_dtype(self, value):
        """Return the data type of the passed value."""
        if isinstance(value, models.Model):
            return 'FKEY'
        if isinstance(value, HistoricalDate):
            return 'DATE'
        if isinstance(value, (list | tuple | dict)):
            return 'JSON'
        return type(value).__name__.upper()


class AFHasKeyLookup(HasKeyLookup):
    def as_sql(self, compiler, connection, template=None):
        # Process JSON path from the left-hand side.
        if isinstance(self.lhs, AFKeyTransform):
            lhs, lhs_params, lhs_key_transforms = self.lhs.preprocess_lhs(compiler, connection)
            lhs_json_path = compile_json_path(lhs_key_transforms)
        else:
            lhs, lhs_params = self.process_lhs(compiler, connection)
            lhs_json_path = '$'

        sql = template % lhs

        # Process JSON path from the right-hand side.
        rhs = self.rhs
        rhs_params = []

        if not isinstance(rhs, list | tuple):
            rhs = [rhs]

        for key in rhs:
            if isinstance(key, AFKeyTransform):
                *_, rhs_key_transforms = key.preprocess_lhs(compiler, connection)
            else:
                rhs_key_transforms = [key]
            *rhs_key_transforms, final_key = rhs_key_transforms
            rhs_json_path = compile_json_path(rhs_key_transforms, include_root=False)
            rhs_json_path += self.compile_json_path_final_key(final_key)
            rhs_params.append(lhs_json_path + rhs_json_path)

        # Add condition for each key.
        if self.logical_operator:
            sql = '(%s)' % self.logical_operator.join([sql] * len(rhs_params))

        return sql, tuple(lhs_params) + tuple(rhs_params)

    def as_postgresql(self, compiler, connection):
        if isinstance(self.rhs, AFKeyTransform):
            *_, rhs_key_transforms = self.rhs.preprocess_lhs(compiler, connection)
            for key in rhs_key_transforms[:-1]:
                self.lhs = AFKeyTransform(key, self.lhs)
            self.rhs = rhs_key_transforms[-1]
        return super().as_postgresql(compiler, connection)


class AFHasKey(AFHasKeyLookup, HasKey):
    pass


class AFHasKeys(AFHasKeyLookup, HasKeys):
    pass


class AFHasAnyKeys(AFHasKeys, HasAnyKeys):
    pass


class AFHasKeyOrArrayIndex(AFHasKey, HasKeyOrArrayIndex):
    pass


class AFExact(lookups.Exact):
    def process_lhs(self, compiler, connection, lhs=None):
        if self.lhs and not isinstance(self.lhs, AFKeyTransform):
            self.lhs = AFKeyTransform('value', self.lhs)
        lhs_sql, params = super().process_lhs(compiler, connection, lhs)
        return lhs_sql, list(params)

    def process_rhs(self, compiler, connection):
        rhs, rhs_params = super().process_rhs(compiler, connection)
        # Treat None lookup values as null.
        if rhs == '%s' and rhs_params == [None]:
            rhs_params = ['null']
        return rhs, rhs_params


class AFIContains(CaseInsensitiveMixin, lookups.IContains):
    pass


AttributeField.register_lookup(DataContains)
AttributeField.register_lookup(ContainedBy)
AttributeField.register_lookup(AFHasKey)
AttributeField.register_lookup(AFHasKeys)
AttributeField.register_lookup(AFHasAnyKeys)
AttributeField.register_lookup(AFExact)
AttributeField.register_lookup(AFIContains)


class AFKeyTransform(KeyTransform):
    def preprocess_lhs(self, compiler, connection):  # noqa: ARG002
        key_transforms = [self.key_name]
        previous = self.lhs
        while isinstance(previous, AFKeyTransform):
            key_transforms.insert(0, previous.key_name)
            previous = previous.lhs
        lhs, params = compiler.compile(previous)
        # if needed, inject 'value'
        if key_transforms[0] != 'value':
            key_transforms.insert(0, 'value')
        return lhs, params, key_transforms


class AFKeyTextTransform(AFKeyTransform, KeyTextTransform):
    pass


class AFKeyTransformTextLookupMixin(KeyTransformTextLookupMixin):
    def __init__(self, key_transform, *args, **kwargs):
        if not isinstance(key_transform, AFKeyTransform):
            msg = 'Transform should be an instance of AttributeKeyTransform in order to use this lookup.'
            raise TypeError(msg)
        key_text_transform = AFKeyTextTransform(
            key_transform.key_name,
            *key_transform.source_expressions,
            **key_transform.extra,
        )
        super().__init__(key_text_transform, *args, **kwargs)


class AFKeyTransformIsNull(lookups.IsNull):
    pass


class AFKeyTransformIn(lookups.In):
    pass


class AFKeyTransformExact(AFExact):
    def process_rhs(self, compiler, connection):
        if isinstance(self.rhs, AFKeyTransform):
            return super(lookups.Exact, self).process_rhs(compiler, connection)
        rhs, rhs_params = super().process_rhs(compiler, connection)
        return rhs, rhs_params


class AFKeyTransformIExact(CaseInsensitiveMixin, AFKeyTransformTextLookupMixin, lookups.IExact):
    pass


class AFKeyTransformIContains(CaseInsensitiveMixin, AFKeyTransformTextLookupMixin, lookups.IContains):
    pass


class AFKeyTransformStartsWith(AFKeyTransformTextLookupMixin, lookups.StartsWith):
    pass


class AFKeyTransformIStartsWith(CaseInsensitiveMixin, AFKeyTransformTextLookupMixin, lookups.IStartsWith):
    pass


class AFKeyTransformEndsWith(AFKeyTransformTextLookupMixin, lookups.EndsWith):
    pass


class AFKeyTransformIEndsWith(CaseInsensitiveMixin, AFKeyTransformTextLookupMixin, lookups.IEndsWith):
    pass


class AFKeyTransformRegex(AFKeyTransformTextLookupMixin, lookups.Regex):
    pass


class AFKeyTransformIRegex(CaseInsensitiveMixin, AFKeyTransformTextLookupMixin, lookups.IRegex):
    pass


class AFKeyTransformNumericLookupMixin(KeyTransformNumericLookupMixin):
    pass


class AFKeyTransformLt(AFKeyTransformNumericLookupMixin, lookups.LessThan):
    pass


class AFKeyTransformLte(AFKeyTransformNumericLookupMixin, lookups.LessThanOrEqual):
    pass


class AFKeyTransformGt(AFKeyTransformNumericLookupMixin, lookups.GreaterThan):
    pass


class AFKeyTransformGte(AFKeyTransformNumericLookupMixin, lookups.GreaterThanOrEqual):
    pass


AFKeyTransform.register_lookup(AFKeyTransformIn)
AFKeyTransform.register_lookup(AFKeyTransformExact)
AFKeyTransform.register_lookup(AFKeyTransformIExact)
AFKeyTransform.register_lookup(AFKeyTransformIsNull)
AFKeyTransform.register_lookup(AFKeyTransformIContains)
AFKeyTransform.register_lookup(AFKeyTransformStartsWith)
AFKeyTransform.register_lookup(AFKeyTransformIStartsWith)
AFKeyTransform.register_lookup(AFKeyTransformEndsWith)
AFKeyTransform.register_lookup(AFKeyTransformIEndsWith)
AFKeyTransform.register_lookup(AFKeyTransformRegex)
AFKeyTransform.register_lookup(AFKeyTransformIRegex)
AFKeyTransform.register_lookup(AFKeyTransformLt)
AFKeyTransform.register_lookup(AFKeyTransformLte)
AFKeyTransform.register_lookup(AFKeyTransformGt)
AFKeyTransform.register_lookup(AFKeyTransformGte)


class AFKeyTransformFactory(KeyTransformFactory):
    def __call__(self, *args, **kwargs):
        return AFKeyTransform(self.key_name, *args, **kwargs)
