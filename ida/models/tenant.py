"""Multitenancy-related models."""

from django_tenants.models import DomainMixin, TenantMixin

from django.conf import settings
from django.db import models

from ida.models.templates import IDAIntid


class Tenant(IDAIntid, TenantMixin):
    """Multi-tenancy functionality table."""

    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)


class Domain(IDAIntid, DomainMixin):
    """Table mapping tenants to domains."""
