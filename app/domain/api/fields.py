"""Define custom API fields."""

import importlib
import inspect

from rest_framework.fields import Field
from rest_framework.serializers import BaseSerializer


def _signature_parameters(func):
    try:
        inspect.signature  # noqa: B018
    except AttributeError:
        return inspect.getargspec(func).args
    else:
        return inspect.signature(func).parameters.keys()


class RecursiveField(Field):
    """A field that gets its representation from its parent.

    Based on: https://github.com/heywbj/django-rest-framework-recursive/tree/master

    """

    # attributes `rest_framework.serializers` calls to on a field object
    PROXIED_ATTRS = (
        # methods
        'get_value',
        'get_initial',
        'run_validation',
        'get_attribute',
        'to_representation',
        # attributes
        'field_name',
        'source',
        'read_only',
        'default',
        'source_attrs',
        'write_only',
    )

    def __init__(self, to=None, **kwargs):
        """Override the default constructor."""
        # to - `None`, the name of another serializer defined in the same module
        # as this serializer, or the fully qualified import path to another serializer

        self.to = to
        self.init_kwargs = kwargs
        self._proxied = None

        super_kwargs = {key: kwargs[key] for key in kwargs if key in _signature_parameters(Field.__init__)}
        super().__init__(**super_kwargs)

    def bind(self, field_name, parent):
        # Extra-lazy binding, because when we are nested in a ListField, the
        # RecursiveField will be bound before the ListField is bound
        self.bind_args = (field_name, parent)

    @property
    def proxied(self):
        if not self._proxied and self.bind_args:
            field_name, parent = self.bind_args

            if hasattr(parent, 'child') and parent.child is self:
                # RecursiveField nested inside of a ListField
                parent_class = parent.parent.__class__
            else:
                # RecursiveField directly inside a Serializer
                parent_class = parent.__class__

            assert issubclass(parent_class, BaseSerializer)

            if self.to is None:
                proxied_class = parent_class
            else:
                try:
                    module_name, class_name = self.to.rsplit('.', 1)
                except ValueError:
                    module_name, class_name = parent_class.__module__, self.to

                try:
                    proxied_class = getattr(importlib.import_module(module_name), class_name)
                except Exception as e:
                    msg = f'could not locate serializer {self.to}'
                    raise ImportError(msg, e) from e

            # Create a new serializer instance and proxy it
            proxied = proxied_class(**self.init_kwargs)
            proxied.bind(field_name, parent)
            self._proxied = proxied

        return self._proxied

    def __getattribute__(self, name):
        if name in RecursiveField.PROXIED_ATTRS:
            try:
                proxied = object.__getattribute__(self, 'proxied')
                return getattr(proxied, name)
            except AttributeError:
                pass

        return object.__getattribute__(self, name)
