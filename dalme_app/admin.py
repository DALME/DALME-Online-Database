""" This file is where all of the admin interface views are set up, available at /admin """

from django.contrib import admin
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from .models import GroupProperties


class GPInline(admin.StackedInline):
    model = GroupProperties
    can_delete = False
    verbose_name_plural = 'properties'


class GroupAdmin(BaseGroupAdmin):
    inlines = (GPInline, )


admin.site.register(Permission)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
