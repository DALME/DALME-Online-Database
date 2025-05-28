"""Define model factories for the app app."""

from unittest import mock

import factory

from django.db import models

from app.abstract import OwnedMixin, TrackingMixin, UuidMixin


def save_parent_override(obj, *args, **kwargs):  # noqa: ARG001
    """Override Django's model.Model save method to prevent actual database operations."""
    return obj


@mock.patch('django.db.models.Model.save', save_parent_override)
def save_model_override(obj, *args, **kwargs):
    """Override save method in local model to simulate updates in factory objects."""
    is_update = kwargs.pop('is_update', False)
    if is_update:
        obj._state.adding = False  # noqa: SLF001
    super(obj.__class__, obj).save(*args, **kwargs)
    return obj


def get_new_model(name, base_class):
    """Return a concrete model class for testing.

    We build the models dynamically to avoid namespace conflicts.

    Args:
        name: The name of the model class.
        base_class: The base class to inherit from, typically a mixin.

    Returns:
        A new model class with the specified name and base class.

    """
    return type(
        name,
        (base_class,),
        {
            'name': models.CharField(max_length=100),
            '__module__': __name__,
            'Meta': type('Meta', (), {'app_label': 'abstract'}),
            'save': save_model_override,  # Override the save method to use our custom logic
        },
    )


class GenericModelFactory(factory.django.DjangoModelFactory):
    """Generate generic model fixtures."""

    class Meta:
        abstract = True

    name = factory.Sequence(lambda n: 'Owned %03d' % n)  # noqa: UP031

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create an instance of the model using the parent classes' save method."""
        obj = model_class(*args, **kwargs)
        obj.save()
        return obj


class OwnedModelFactory(GenericModelFactory):
    """Generate owned model fixtures."""

    class Meta:
        model = get_new_model('TestOwned', OwnedMixin)


class UUIDModelFactory(GenericModelFactory):
    """Generate UUID model fixtures."""

    class Meta:
        model = get_new_model('TestUUID', UuidMixin)


class TrackedModelFactory(GenericModelFactory):
    """Generate tracked model fixtures."""

    class Meta:
        model = get_new_model('TestTracked', TrackingMixin)
