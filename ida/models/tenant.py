"""Model multitenancy data."""
from django_tenants.models import DomainMixin, TenantMixin

from django.conf import settings
from django.db import models

from dalme_app.models.templates import dalmeIntid


class Tenant(dalmeIntid, TenantMixin):
    """Multi-tenancy functionality table."""

    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)


class Domain(dalmeIntid, DomainMixin):
    """Table mapping tenants to domains."""
