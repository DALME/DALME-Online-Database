"""Multitenancy-related models."""

from django_tenants.models import DomainMixin, TenantMixin

from django.conf import settings
from django.db import models

from ida.models.abstract import TrackingMixin


class Tenant(TrackingMixin, TenantMixin):
    """Multi-tenancy functionality table."""

    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)


class Domain(TrackingMixin, DomainMixin):
    """Table mapping tenants to domains."""
