import json
import pathlib

from rest_access_policy import AccessPolicy, AccessPolicyException

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from dalme_app.models import Permission


class BaseAccessPolicy(AccessPolicy):
    """Base subclass of AccessPolicy to enable loading policy statements from external sources."""

    id = 'base-policy'  # noqa: A003
    permissions = {}
    targets = []
    fail_target_string = None
    error = None
    perm_types = ['can_view', 'can_edit', 'can_delete', 'can_add', 'can_remove']

    def _evaluate_statements(self, statements, request, view, action):
        result = super()._evaluate_statements(statements, request, view, action)
        if not result:
            if self.error is not None:
                self.message = f'Error: {self.error}'

            else:
                if self.fail_target_string is None:
                    self.fail_target_string = 'one or more of these records' if len(self.targets) > 1 else 'this record'

                action_string = f" ({action.replace('bulk_', '')})" if action is not None else ''

                self.message = 'You do not have permission to perform the requested action{} on {}.'.format(
                    action_string,
                    self.fail_target_string,
                )
        return result

    def _get_invoked_action(self, view):
        if hasattr(view, "action"):
            if view.action == 'has_permission':
                return 'update'
            return view.action

        if hasattr(view, "__class__"):
            if view.__class__.__name__ in ['RecordDetail', 'dict']:
                return 'update'
            return view.__class__.__name__

        msg = 'Could not determine action of request'
        raise AccessPolicyException(msg)

    def get_policy_statements(self, request, view):  # noqa: ARG002
        """Load policy statements."""
        with pathlib.Path(f'static/policies/{self.id}.json').open() as policy:
            return json.load(policy)

    def get_parent(self, target):
        """Return parent object. Should be overwritten by subclasses to provide resource-specific parents."""
        return (target, self)

    def get_targets(self, view, arg=None):
        """Return target object(s)."""
        if len(self.targets) == 0:
            if type(view) is dict:
                self.targets = [view.get('object', {})]

            elif hasattr(view, 'object'):
                self.targets = [view.object]

            elif hasattr(view, 'get_object'):
                try:
                    self.targets = [view.get_object()]
                except AssertionError:
                    objects = []
                    for t_id in list(view.request.data.keys()):
                        view.kwargs['pk'] = t_id
                        objects.append(view.get_object())
                    self.targets = objects
            else:
                self.targets = [{}]

            if arg == 'parent_as_proxy':
                self.targets = [self.get_parent(target) for target in self.targets]

        return self.targets

    def get_permissions(self, request, view):
        """Return explicit object-level permissions."""
        if not self.permissions:
            permissions = {}
            user = request.user
            user_groups = user.groups.all()
            group_ids = [g.id for g in user_groups]
            ct_group = ContentType.objects.get_for_model(user_groups[0])
            ct_user = ContentType.objects.get_for_model(user)

            for target in self.get_targets(view):
                ct_content = ContentType.objects.get_for_model(target)
                default_perms = Q(
                    object_id=target.id,
                    content_type=ct_content,
                    is_default=True,
                )
                user_perms = Q(
                    object_id=target.id,
                    content_type=ct_content,
                    principal_type=ct_user,
                    principal_id=user.id,
                )
                group_perms = Q(
                    object_id=target.id,
                    content_type=ct_content,
                    principal_type=ct_group,
                    principal_id__in=group_ids,
                )
                perm_obj = Permission.objects.filter(default_perms | user_perms | group_perms).values(*self.perm_types)

                permissions[target.id] = {}
                for pt in self.perm_types:
                    permissions[target.id][pt] = len([i[pt] for i in perm_obj if i[pt] is True]) > 0

            self.permissions = permissions

        return self.permissions

    def user_must_be(self, request, view, action, arg=None):  # noqa: ARG002
        """Test 'user_must_be' condition."""
        if arg is None:
            self.error = '"user_must_be" condition requires a parameter, none was supplied.'
            return False

        if arg in ['owner', 'creator', 'self']:
            for target in self.get_targets(view):
                try:
                    test = target.owner if arg == 'owner' else target.creation_user if arg == 'creator' else target
                    if request.user != test:
                        self.fail_target_string = target.get('name')
                        return False

                except Exception as e:  # noqa: BLE001
                    self.error = str(e)
                    return False

            return True

        self.error = f'{arg} is not a valid argument for the "user_must_be" condition.'
        return False

    def has_perm(self, request, view, action, arg=None):  # noqa: ARG002
        """Test 'has_perm' condition."""
        if arg is None:
            self.error = '"has_perm" condition requires a parameter, none was supplied.'
            return False

        if arg not in self.perm_types:
            self.error = f'{arg} is not a valid argument for the "has_perm" condition. Must be one of {", ".join(self.perm_types)}'
            return False

        perms = self.get_permissions(request, view)
        for target in self.get_targets(view):
            try:
                if not perms.get(target.id, {}).get(arg):
                    self.fail_target_string = target.get('name')
                    return False

            except Exception as e:  # noqa: BLE001
                self.error = str(e)
                return False

        return True

    def parent_as_proxy(self, request, view, action):  # noqa: ARG002
        """Test permissions using object's parent as proxy."""
        targets = [self.get_parent(t) for t in self.get_targets(view)]
        for target, cls in targets:
            try:
                if cls.has_permission(request, {'object': target}) is False:
                    self.fail_target_string = target.get('name')
                    return False

            except Exception as e:  # noqa: BLE001
                self.error = str(e)
                return False

        return True


class AgentAccessPolicy(BaseAccessPolicy):
    """Access policies for Agents endpoint."""

    id = 'agents-policy'  # noqa: A003


class AttachmentAccessPolicy(BaseAccessPolicy):
    """Access policies for Attachments endpoint."""

    id = 'attachments-policy'  # noqa: A003


class AttributeAccessPolicy(BaseAccessPolicy):
    """Access policies for record attributes."""

    id = 'attributes-policy'  # noqa: A003


class CollectionAccessPolicy(BaseAccessPolicy):
    """Access policies for Collections endpoint."""

    id = 'collections-policy'  # noqa: A003


class CommentAccessPolicy(BaseAccessPolicy):
    """Access policies for Comments endpoint."""

    id = 'comments-policy'  # noqa: A003


class GeneralAccessPolicy(BaseAccessPolicy):
    """General-purpose access policies."""

    id = 'general-policy'  # noqa: A003


class ImageAccessPolicy(BaseAccessPolicy):
    """Access policies for Images endpoint."""

    id = 'images-policy'  # noqa: A003


class LibraryAccessPolicy(BaseAccessPolicy):
    """Access policies for Library endpoint."""

    id = 'library-policy'  # noqa: A003


class LocaleAccessPolicy(BaseAccessPolicy):
    """Access policies for Locales endpoint."""

    id = 'locales-policy'  # noqa: A003


class PageAccessPolicy(BaseAccessPolicy):
    """Access policies for Pages endpoint."""

    id = 'pages-policy'  # noqa: A003

    def get_parent(self, target):
        """Return page parent object (record)."""
        return (target.records.all()[0].record, RecordAccessPolicy())


class PlaceAccessPolicy(BaseAccessPolicy):
    """Access policies for Places endpoint."""

    id = 'places-policy'  # noqa: A003


class PublicAccessPolicy(BaseAccessPolicy):
    """Access policies for public site."""

    id = 'public-policy'  # noqa: A003


class RightsAccessPolicy(BaseAccessPolicy):
    """Access policies for Rights endpoint."""

    id = 'rights-policy'  # noqa: A003


class RecordAccessPolicy(BaseAccessPolicy):
    """Access policies for Records endpoint."""

    id = 'records-policy'  # noqa: A003

    @classmethod
    def scope_queryset(cls, request, queryset):
        """Return filtered queryset based on permissions."""
        if request.user.is_superuser:
            return queryset

        return queryset.filter(is_private=False)


class SessionAccessPolicy(BaseAccessPolicy):
    """Access policies for Session endpoint."""

    id = 'session-policy'  # noqa: A003


class TaskAccessPolicy(BaseAccessPolicy):
    """Access policies for Tasks endpoint."""

    id = 'tasks-policy'  # noqa: A003


class TaskListAccessPolicy(BaseAccessPolicy):
    """Access policies for Tasks Lists endpoint."""

    id = 'task_lists-policy'  # noqa: A003


class TranscriptionAccessPolicy(BaseAccessPolicy):
    """Access policies for Transcriptions endpoint."""

    id = 'transcriptions-policy'  # noqa: A003

    def get_parent(self, target):
        """Return transcription parent object (record)."""
        return (target.folios.all()[0].record, RecordAccessPolicy())


class TicketAccessPolicy(BaseAccessPolicy):
    """Access policies for Tickets endpoint."""

    id = 'tickets-policy'  # noqa: A003


class WorkflowAccessPolicy(BaseAccessPolicy):
    """Access policies for Workflow endpoint."""

    id = 'workflow-policy'  # noqa: A003

    def get_parent(self, target):
        """Return workflow parent object (record)."""
        return (target.record, RecordAccessPolicy())


class UserAccessPolicy(BaseAccessPolicy):
    """Access policies for Users endpoint."""

    id = 'users-policy'  # noqa: A003
