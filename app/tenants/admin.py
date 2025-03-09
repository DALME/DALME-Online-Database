"""Register models with the Django admin for the IDA."""

from django_tenants.admin import TenantAdminMixin

from django.contrib import admin

from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    """Tenant admin."""

    list_display = ('id', 'name', 'schema_name')

    def has_delete_permission(self, request, obj=None):  # noqa: ARG002
        """Don't allow deletion of Tenants from the admin."""
        return False
