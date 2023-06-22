from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group, Permission

from .models import GroupProperties


class GPInline(admin.StackedInline):
    """Group properties."""

    model = GroupProperties
    can_delete = False
    verbose_name_plural = 'properties'


class GroupAdmin(BaseGroupAdmin):
    """Group admin."""

    inlines = (GPInline,)


admin.site.register(Permission)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
