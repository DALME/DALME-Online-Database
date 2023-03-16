"""Model tenant data."""
from django_tenants.models import DomainMixin, TenantMixin

from django.db import models

from dalme_app.models.templates import dalmeIntid


class TenantRoleChoices(models.TextChoices):
    """Enumerate the Tenant user roles."""

    ADMIN = 'admin', 'Admin'
    MEMBER = 'member', 'Member'


class TenantRole(dalmeIntid):
    """Authorization roles for a Tenant."""

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tenant', 'user'],
                name='uq_tenant_role_tenant_user',
            ),
        ]

    level = models.CharField(
        max_length=6,
        choices=TenantRoleChoices.choices,
        default=TenantRoleChoices.MEMBER,
    )

    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class Tenant(dalmeIntid, TenantMixin):
    """Multi-tenancy functionality table."""

    name = models.CharField(max_length=255, unique=True)


class Domain(dalmeIntid, DomainMixin):
    """Table mapping tenants to domains."""
