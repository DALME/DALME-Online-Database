"""Mixin for assigning permissions to model instances."""

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q

from domain.models.permission import PERMISSION_TYPES, Permission


class PermissionMixin(models.Model):
    permissions = GenericRelation(
        'domain.Permission',
        related_query_name='%(app_label)s_%(class)s_related',
    )

    class Meta:
        abstract = True

    def get_user_permissions(self, user):
        permissions = {}
        user_groups = user.groups_scoped
        group_ids = [g.id for g in user_groups]
        ct_group = ContentType.objects.get_for_model(user_groups[0])
        ct_user = ContentType.objects.get_for_model(user)
        ct_content = ContentType.objects.get_for_model(self)
        default_perms = Q(
            object_id=self.id,
            content_type=ct_content,
            is_default=True,
        )
        user_perms = Q(
            object_id=self.id,
            content_type=ct_content,
            principal_type=ct_user,
            principal_id=user.id,
        )
        group_perms = Q(
            object_id=self.id,
            content_type=ct_content,
            principal_type=ct_group,
            principal_id__in=group_ids,
        )
        perm_obj = Permission.objects.filter(default_perms | user_perms | group_perms).values(*PERMISSION_TYPES)

        for pt in PERMISSION_TYPES:
            permissions[pt] = len([i[pt] for i in perm_obj if i[pt] is True]) > 0

        return permissions
