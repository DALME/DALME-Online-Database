"""Base serializer functionality."""

from rest_framework import serializers


class DynamicSerializer(serializers.ModelSerializer):
    """A serializer that takes an additional `fields` argument that indicates which fields should be included."""

    def __init__(self, *args, **kwargs):
        if 'fields' in kwargs and 'field_set' in kwargs:
            msg = '`fields` and `field_set` cannot be used concurrently.'
            raise AssertionError(msg)

        fields = kwargs.pop('fields', None)
        field_set = kwargs.pop('field_set', None)
        super().__init__(*args, **kwargs)

        if field_set is not None:
            assert hasattr(self.Meta, 'field_sets'), (
                'Use of `field_set` requires the `field_sets` dictionary to be defined in the class `Meta`.',
            )
            fields = self.Meta.field_sets.get(field_set)

        if fields is not None:
            set_fields = dict(self.fields)
            for k, _v in set_fields.items():
                if k not in fields:
                    self.fields.pop(k)
