"""Register models with the Django admin."""
from django_tenants.admin import TenantAdminMixin

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group, Permission

from .models import GroupProperties, Tenant


class GPInline(admin.StackedInline):
    """Group properties."""

    model = GroupProperties
    can_delete = False
    verbose_name_plural = 'properties'


class GroupAdmin(BaseGroupAdmin):
    """Group admin."""

    inlines = (GPInline,)


class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name',)


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(Permission)
admin.site.register(Tenant)
