"""Register models with the Django admin."""
from django_tenants.admin import TenantAdminMixin

from django.contrib import admin

from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name',)
