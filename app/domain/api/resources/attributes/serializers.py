"""Serializers for attribute data."""

from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty
from rest_framework.settings import api_settings
from rest_framework.utils import html

from django.db import models

from domain.api.serializers import DynamicSerializer
from domain.models import Attribute, AttributeType, ContentAttributes, ContentTypeExtended


class AttributeTypeSerializer(serializers.ModelSerializer):
    """Serializer for attribute types."""

    class Meta:
        model = AttributeType
        fields = [
            'id',
            'name',
            'label',
            'description',
            'data_type',
            'source',
            'options',
            'same_as',
        ]


class AttributeListSerializer(serializers.ListSerializer):
    """Overrides basic list serializer to ensure item serializer is initialized for each instance."""

    def __init__(self, *args, **kwargs):
        self.child = kwargs.pop('child', None)
        self.allow_empty = kwargs.pop('allow_empty', True)
        self.max_length = kwargs.pop('max_length', None)
        self.min_length = kwargs.pop('min_length', None)

        instance = kwargs.get('instance', [])
        data = kwargs.get('data', [])
        if instance and data:
            assert len(data) == len(instance), 'Data and instance should have same length'

        super(serializers.ListSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, data):
        """Override method to use serializer class instead of instance."""
        iterable = data.all() if isinstance(data, models.manager.BaseManager) else data
        return [self.child(item).data for item in iterable]

    def to_internal_value(self, data):
        """Override method to use serializer class instead of instance."""
        if html.is_html_input(data):
            data = html.parse_html_list(data, default=[])

        if not isinstance(data, list):
            message = self.error_messages['not_a_list'].format(input_type=type(data).__name__)
            raise ValidationError({api_settings.NON_FIELD_ERRORS_KEY: [message]}, code='not_a_list')

        if not self.allow_empty and len(data) == 0:
            message = self.error_messages['empty']
            raise ValidationError({api_settings.NON_FIELD_ERRORS_KEY: [message]}, code='empty')

        if self.max_length is not None and len(data) > self.max_length:
            message = self.error_messages['max_length'].format(max_length=self.max_length)
            raise ValidationError({api_settings.NON_FIELD_ERRORS_KEY: [message]}, code='max_length')

        if self.min_length is not None and len(data) < self.min_length:
            message = self.error_messages['min_length'].format(min_length=self.min_length)
            raise ValidationError({api_settings.NON_FIELD_ERRORS_KEY: [message]}, code='min_length')

        ret = []
        errors = []

        for _idx, item in enumerate(data):
            # if hasattr(self, 'instance') and self.instance and len(self.instance) > idx:
            #     self.child.instance = self.instance[idx]
            try:
                serializer = self.child(item)
                assert serializer.is_valid(raise_exception=True) is True
            except ValidationError as exc:
                errors.append(exc.detail)
            else:
                ret.append(serializer.validated_data)
                errors.append({})

        if any(errors):
            raise ValidationError(errors)

        return ret


class AttributeDateSerializer(serializers.Serializer):
    """Serializer for attribute date information."""

    day = serializers.IntegerField(max_value=31, min_value=1)
    month = serializers.IntegerField(max_value=12, min_value=1)
    year = serializers.IntegerField()
    # for use, e.g. with luxon as DateTime.fromISO("2016-05-25")
    date = serializers.DateField(format='iso-8601', input_formats=['iso-8601'])
    text = serializers.CharField(trim_whitespace=True)


class AttributeSerializer(DynamicSerializer, WritableNestedModelSerializer):
    """Serializer for attribute data."""

    id = serializers.ReadOnlyField()
    attribute_type = serializers.ReadOnlyField(source='attribute_type.id')
    name = serializers.ReadOnlyField(source='attribute_type.name')
    label = serializers.ReadOnlyField(source='attribute_type.label')
    description = serializers.ReadOnlyField(source='attribute_type.description')
    data_type = serializers.ReadOnlyField(source='attribute_type.data_type')

    class Meta:
        model = Attribute
        fields = [
            'id',
            'name',
            'label',
            'description',
            'value',
            'attribute_type',
            'data_type',
        ]

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)

        if not isinstance(instance, list) or not isinstance(data, list):
            data_type = (
                self.instance.data_type
                if instance is not None
                else self.initial_data.get('data_type')
                if data is not empty
                else None
            )

            if data_type == 'BOOL':
                self.fields['value'] = serializers.BooleanField()
            elif data_type == 'DATE':
                self.fields['value'] = AttributeDateSerializer()
            elif data_type == 'FLOAT':
                self.fields['value'] = serializers.FloatField()
            elif data_type == 'INT':
                self.fields['value'] = serializers.IntegerField()
            elif data_type == 'JSON':
                self.fields['value'] = serializers.JSONField()
            elif data_type == 'STR':
                self.fields['value'] = serializers.CharField()
            elif data_type == 'FKEY':
                model_name = self.instance.value._meta.model.__name__  # noqa: SLF001
                serializer_class_name = f'{model_name}Serializer'
                srs = __import__('domain.api.resources', fromlist=[serializer_class_name])  # noqa: F841
                serializer_class = eval(f'srs.{serializer_class_name}')
                self.fields['value'] = serializer_class(self.instance.value, field_set='attribute')

    @classmethod
    def many_init(cls, *args, **kwargs):
        """Override method to create a `ListSerializer` parent class when `many=True`."""
        allow_empty = kwargs.pop('allow_empty', None)
        max_length = kwargs.pop('max_length', None)
        min_length = kwargs.pop('min_length', None)
        list_kwargs = {'child': cls}

        if allow_empty is not None:
            list_kwargs['allow_empty'] = allow_empty
        if max_length is not None:
            list_kwargs['max_length'] = max_length
        if min_length is not None:
            list_kwargs['min_length'] = min_length

        list_kwargs.update(
            {key: value for key, value in kwargs.items() if key in serializers.LIST_SERIALIZER_KWARGS},
        )

        return AttributeListSerializer(*args, **list_kwargs)


class ContentTypeSerializer(DynamicSerializer):
    """Serializer for content types."""

    attribute_types = AttributeTypeSerializer(many=True, required=False)

    class Meta:
        model = ContentTypeExtended
        fields = [
            'id',
            'name',
            'description',
            'is_abstract',
            'attribute_types',
            'parent',
            'can_view',
            'can_edit',
            'can_delete',
            'can_add',
            'can_remove',
        ]
        field_sets = {
            'attribute': [
                'id',
                'name',
                'short_name',
                'is_abstract',
                'description',
            ],
        }
        extra_kwargs = {
            'name': {
                'validators': [],
            },
        }


class ContentAttributesSerializer(DynamicSerializer):
    """Serializer for content attributes."""

    content_type = ContentTypeSerializer(required=False)
    attribute_type = AttributeTypeSerializer(required=False)

    class Meta:
        model = ContentAttributes
        fields = [
            'id',
            'content_type',
            'attribute_type',
            'order',
            'required',
            'unique',
        ]
