"""Multitenancy-related models."""

from django_tenants.models import DomainMixin, TenantMixin

from django.conf import settings
from django.db import models

from .templates import IntIdMixin, TrackedMixin


class Tenant(IntIdMixin, TrackedMixin, TenantMixin):
    """Multi-tenancy functionality table."""

    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)


class Domain(IntIdMixin, TrackedMixin, DomainMixin):
    """Table mapping tenants to domains."""
