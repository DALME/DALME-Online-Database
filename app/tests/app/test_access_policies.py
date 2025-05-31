"""Tests for access policies."""

from unittest import mock

import pytest

from app import access_policies


@pytest.mark.django_db
def test_evaluate_statements_sets_message_on_failure(base_policy, mock_request, mock_view_list):
    # Patch super()._evaluate_statements to return False
    with mock.patch.object(access_policies.AccessPolicy, '_evaluate_statements', return_value=False):
        base_policy.targets = [mock.Mock()]
        base_policy.error = None
        result = base_policy._evaluate_statements([], mock_request, mock_view_list, 'test_action')  # noqa: SLF001
        assert result is False
        assert 'You do not have permission' in base_policy.message


@pytest.mark.django_db
def test_evaluate_statements_sets_error_message(base_policy, mock_request, mock_view_list):
    with mock.patch.object(access_policies.AccessPolicy, '_evaluate_statements', return_value=False):
        base_policy.error = 'Some error'
        base_policy.targets = [mock.Mock()]
        result = base_policy._evaluate_statements([], mock_request, mock_view_list, 'test_action')  # noqa: SLF001
        assert result is False
        assert 'Error: Some error' in base_policy.message


def test_get_invoked_action_with_action_attr(base_policy, mock_view_list, mock_view_detail):
    assert base_policy._get_invoked_action(mock_view_list) == 'list'  # noqa: SLF001
    assert base_policy._get_invoked_action(mock_view_detail) == 'detail'  # noqa: SLF001
    mock_view_detail.action = 'has_permission'
    assert base_policy._get_invoked_action(mock_view_detail) == 'update'  # noqa: SLF001


def test_get_invoked_action_with_class_name(base_policy):
    class Dummy:
        pass

    view = Dummy()
    assert base_policy._get_invoked_action(view) == 'Dummy'  # noqa: SLF001
    view.__class__.__name__ = 'RecordDetail'
    assert base_policy._get_invoked_action(view) == 'update'  # noqa: SLF001


@pytest.mark.django_db
def test_get_policy_statements_reads_file(base_policy, mock_request, mock_view_list, tmp_path):
    # Patch settings.PROJECT_ROOT
    with mock.patch.object(access_policies.settings, 'PROJECT_ROOT', tmp_path):
        # Write a fake policy file
        policy_path = tmp_path / 'authorization' / 'policies'
        policy_path.mkdir(parents=True)
        policy_file = policy_path / f'{base_policy.id}.json'
        policy_file.write_text('[{"action": "test"}]')
        statements = base_policy.get_policy_statements(mock_request, mock_view_list)
        assert statements == [{'action': 'test'}]


def test_get_parent_returns_tuple(base_policy):
    target = mock.Mock()
    parent = base_policy.get_parent(target)
    assert parent == (target, base_policy)


def test_get_targets_with_dict(base_policy):
    view = {'object': {'id': 1}}
    base_policy.targets = []
    targets = base_policy.get_targets(view)
    assert targets == [{'id': 1}]


def test_get_targets_with_object_attr(base_policy, mock_view_detail, mock_object_1):
    targets = base_policy.get_targets(mock_view_detail)
    assert targets == [mock_object_1]


def test_get_targets_with_action_list_and_queryset(base_policy, mock_view_list, mock_object_1, mock_object_2):
    targets = base_policy.get_targets(mock_view_list)
    assert not isinstance(mock_view_list, dict)
    assert hasattr(mock_view_list, 'object') is False
    assert isinstance(targets, list)
    assert hasattr(mock_view_list, 'action')
    assert mock_view_list.action == 'list'
    assert len(targets) == 2  # noqa: PLR2004
    assert targets[0].id == mock_object_1.id
    assert targets[1].id == mock_object_2.id
    assert [obj.id for obj in targets] == [mock_object_1.id, mock_object_2.id]


@pytest.mark.django_db
@mock.patch('oauth.models.user.get_current_tenant')
def test_get_permissions_returns_permissions(
    mock_get_current_tenant,
    base_policy,
    mock_view_list,
    test_domain,
    factories,
):
    mock_get_current_tenant.return_value = test_domain.tenant
    groups = factories.user_groups.create_batch(3)
    user = factories.users.create(groups=groups)
    request = mock.Mock()
    request.user = user
    request.access_enforcement = None
    fake_target = mock.Mock(id=1)
    base_policy.targets = [fake_target]
    mock_view_list.object = fake_target
    # Patch ContentType and Permission
    with (
        mock.patch.object(access_policies.ContentType.objects, 'get_for_model', return_value='ct'),
        mock.patch.object(access_policies, 'PERMISSION_TYPES', ['can_view', 'can_edit']),
        mock.patch.object(
            access_policies.Permission.objects,
            'filter',
            return_value=mock.Mock(values=lambda *a: [{'can_view': True, 'can_edit': False}]),  # noqa: ARG005
        ),
    ):
        perms = base_policy.get_permissions(request, mock_view_list)
        assert perms[1]['can_view'] is True
        assert perms[1]['can_edit'] is False


@pytest.mark.django_db
def test_user_must_be_success(base_policy, mock_request, mock_view_list):
    fake_target = mock.Mock()
    fake_target.owner = mock_request.user
    base_policy.targets = [fake_target]
    assert base_policy.user_must_be(mock_request, mock_view_list, None, 'owner') is True


@pytest.mark.django_db
def test_user_must_be_fail(base_policy, mock_request, mock_view_list):
    fake_target = mock.Mock()
    fake_target.owner = mock.Mock()
    base_policy.targets = [fake_target]
    assert base_policy.user_must_be(mock_request, mock_view_list, None, 'owner') is False
    assert base_policy.fail_target_string is not None


@pytest.mark.django_db
def test_user_must_be_no_arg(base_policy, mock_request, mock_view_list):
    base_policy.targets = []
    assert base_policy.user_must_be(mock_request, mock_view_list, None) is False
    assert 'requires a parameter' in base_policy.error


@pytest.mark.django_db
def test_has_perm_success(base_policy, mock_request, mock_view_list):
    base_policy.targets = [mock.Mock(id=1)]
    base_policy.permissions = {1: {'can_view': True}}
    with mock.patch.object(access_policies, 'PERMISSION_TYPES', ['can_view']):
        assert base_policy.has_perm(mock_request, mock_view_list, None, 'can_view') is True


@pytest.mark.django_db
def test_has_perm_invalid_arg(base_policy, mock_request, mock_view_list):
    base_policy.targets = [mock.Mock(id=1)]
    with mock.patch.object(access_policies, 'PERMISSION_TYPES', ['can_view']):
        assert base_policy.has_perm(mock_request, mock_view_list, None, 'bad_perm') is False
        assert 'not a valid argument' in base_policy.error


@pytest.mark.django_db
def test_include_restricted_fields_true(base_policy, mock_request, mock_view_list):
    with (
        mock.patch.object(base_policy, 'get_policy_statements', return_value=[{'action': 'include_restricted_fields'}]),
        mock.patch.object(base_policy, '_evaluate_statements', return_value=True),
    ):
        allowed = base_policy.include_restricted_fields(mock_request, mock_view_list)
        assert allowed is True
        assert hasattr(mock_request, 'access_enforcement')


@pytest.mark.django_db
def test_include_restricted_fields_false(base_policy, mock_request, mock_view_list):
    with mock.patch.object(base_policy, 'get_policy_statements', return_value=[]):
        allowed = base_policy.include_restricted_fields(mock_request, mock_view_list)
        assert allowed is False


@pytest.mark.django_db
def test_parent_as_proxy_success(base_policy, mock_request, mock_view_list):
    fake_target = mock.Mock()
    base_policy.targets = [fake_target]
    with (
        mock.patch.object(base_policy, 'get_parent', return_value=(fake_target, base_policy)),
        mock.patch.object(base_policy, 'has_permission', return_value=True),
    ):
        assert base_policy.parent_as_proxy(mock_request, mock_view_list, None) is True


@pytest.mark.django_db
def test_parent_as_proxy_fail(base_policy, mock_request, mock_view_list):
    fake_target = mock.Mock()
    base_policy.targets = [fake_target]
    with (
        mock.patch.object(base_policy, 'get_parent', return_value=(fake_target, base_policy)),
        mock.patch.object(base_policy, 'has_permission', return_value=False),
    ):
        assert base_policy.parent_as_proxy(mock_request, mock_view_list, None) is False


def test_record_access_policy_scope_queryset_superuser():
    policy = access_policies.RecordAccessPolicy()
    request = mock.Mock()
    request.user.is_superuser = True
    queryset = mock.Mock()
    result = policy.scope_queryset(request, queryset)
    assert result == queryset


def test_record_access_policy_scope_queryset_non_superuser():
    policy = access_policies.RecordAccessPolicy()
    request = mock.Mock()
    request.user.is_superuser = False
    queryset = mock.Mock()
    # Patch annotate and filter
    queryset.annotate.return_value = queryset
    queryset.filter.return_value = 'filtered'
    with mock.patch.object(access_policies.Permission.objects, 'filter', return_value=mock.Mock()):
        result = policy.scope_queryset(request, queryset)
        assert result == 'filtered'
