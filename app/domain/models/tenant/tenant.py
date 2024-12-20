"""Multitenancy-related models."""

from django_tenants.models import DomainMixin, TenantMixin
from django_tenants.utils import get_tenant_type_choices

from django.conf import settings
from django.db import models

from domain.models.abstract import TrackingMixin


class Tenant(TrackingMixin, TenantMixin):
    """Multi-tenancy functionality table."""

    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    tenant_type = models.CharField(max_length=100, choices=get_tenant_type_choices(), default='project')


class Domain(TrackingMixin, DomainMixin):
    """Table mapping tenants to domains."""
