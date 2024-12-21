"""Register models with the Django admin for the IDA."""

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group

from .models import GroupProperties, User
from .models.group import DESCRIPTION_MAX_LENGTH


class ProxyGroup(Group):
    class Meta:
        proxy = True
        verbose_name = 'Group'


class GroupPropertiesInline(admin.StackedInline):
    """Link GroupProperties fields inline on the Group admin."""

    description = forms.CharField(max_length=DESCRIPTION_MAX_LENGTH)

    model = GroupProperties
    fields = ('group_type', 'description')

    def has_delete_permission(self, request, obj=None):  # noqa: ARG002
        """Don't allow deletion of the related GroupProperties object."""
        return False

    def get_formset(self, request, obj=None, **kwargs):
        """Adjust the styling of the inline fields."""
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['description'].widget.attrs['style'] = 'flex: 1; width: 100%;'
        return formset


@admin.register(ProxyGroup)
class GroupAdmin(admin.ModelAdmin):
    """Group admin.

    Integrated with:

    https://github.com/django/django/blob/d9b91e38361696014bdc98434d6d018eae809519/django/contrib/auth/admin.py#L29

    """

    filter_horizontal = ('permissions',)
    list_display = ('id', 'name', 'tenant')
    list_select_related = ('properties',)
    ordering = ('id', 'name')
    search_fields = ('name',)
    inlines = (GroupPropertiesInline,)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        """Bring this logic over from the Django source."""
        if db_field.name == 'permissions':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs['queryset'] = qs.select_related('content_type')
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)

    def tenant(self, group):
        """Join over the group properties to get the group's tenant."""
        return group.properties.tenant


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """User admin."""

    list_display = ('id', 'username', 'full_name', 'email')
