"""Base serializer functionality."""

from rest_framework import serializers


class DynamicSerializer(serializers.ModelSerializer):
    """A serializer that takes an additional `fields` or 'field_set' keyword argument to indicate which fields should be included."""

    def __init__(self, *args, **kwargs):  # noqa: C901
        if 'fields' in kwargs and 'field_set' in kwargs:
            msg = '`fields` and `field_set` cannot be used concurrently.'
            raise ValueError(msg)

        fields = kwargs.pop('fields', None)
        field_set = kwargs.pop('field_set', None)
        action = kwargs.pop('action', None)

        super().__init__(*args, **kwargs)

        if field_set is not None:
            if not hasattr(self.Meta, 'field_sets'):
                msg = 'Use of `field_set` requires `field_sets` dictionary in `Meta`.'
                raise ValueError(msg)

            if isinstance(field_set, (list | tuple)):
                fields = [f for i in field_set for f in self.Meta.field_sets.get(i)]
            else:
                fields = self.Meta.field_sets.get(field_set)

        elif action is not None and hasattr(self.Meta, 'field_sets') and action in self.Meta.field_sets:
            fields = self.Meta.field_sets[action]

        if fields is not None:
            set_fields = dict(self.fields)
            for k, _v in set_fields.items():
                if k not in fields:
                    self.fields.pop(k)

        elif hasattr(self.Meta, 'default_exclude'):
            for field in self.Meta.default_exclude:
                self.fields.pop(field)

        # always include the model field
        self.fields['model'] = serializers.ReadOnlyField(source='_meta.model.__name__')


class PermissionsSerializer(serializers.Serializer):
    """Serializer for object level permissions."""

    can_view = serializers.BooleanField()
    can_edit = serializers.BooleanField()
    can_delete = serializers.BooleanField()
    can_add = serializers.BooleanField()
    can_remove = serializers.BooleanField()

    class Meta:
        fields = [
            'can_view',
            'can_edit',
            'can_delete',
            'can_add',
            'can_remove',
        ]
