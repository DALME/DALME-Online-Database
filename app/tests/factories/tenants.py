"""Define model factories for the tenants app."""

from unittest import mock

import factory

from tenants.models import Domain, Tenant


def save_parent_override(obj, *args, **kwargs):  # noqa: ARG001
    """Override Django's model.Model save method to prevent actual database operations."""
    return obj


@mock.patch('app.abstract.tracking_mixin.TrackingMixin.save', save_parent_override)
def save_model_override(obj, *args, **kwargs):
    """Override save method in local model to simulate updates in factory objects."""
    is_update = kwargs.pop('is_update', False)
    if is_update:
        obj._state.adding = False  # noqa: SLF001
    super(obj.__class__, obj).save(*args, **kwargs)
    return obj


class CustomModelFactory(factory.django.DjangoModelFactory):
    """Generate model fixtures that don't hit the database."""

    class Meta:
        abstract = True

    @classmethod
    @mock.patch('tenants.models.Tenant.save', save_model_override)
    def _create(cls, model_class, *args, **kwargs):
        """Create an instance of the model using the parent classes' save method."""
        obj = model_class(*args, **kwargs)
        obj.save()
        return obj


class TenantModelFactory(CustomModelFactory):
    """Generate tenant model fixtures."""

    class Meta:
        model = Tenant

    id = factory.Sequence(int)


class DomainModelFactory(CustomModelFactory):
    """Generate domain model fixtures."""

    class Meta:
        model = Domain
