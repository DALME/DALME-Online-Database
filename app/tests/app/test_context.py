"""Tests for the app.context module."""

from unittest import mock

from app import context


def test_get_gradient_pages_sets_and_returns_ids():
    mock_app_config = mock.Mock()
    mock_model = mock.Mock()
    mock_model.__name__ = 'TestModel'
    mock_field = mock.Mock()
    mock_field.name = 'gradient'
    mock_model._meta.get_fields.return_value = [mock_field]  # noqa: SLF001
    mock_app_config.models_module = True
    mock_app_config.get_models.return_value = [mock_model]

    with (
        mock.patch('app.context.apps.get_app_config', return_value=mock_app_config),
        mock.patch('app.context.ContentType.objects.filter') as mock_filter,
    ):
        mock_ct = mock.Mock()
        mock_ct.id = 42
        mock_filter.return_value = [mock_ct]
        result = context.get_gradient_pages()
        assert result == [42]
        # Should return cached value on second call
        assert context.get_gradient_pages() == [42]


def test_get_gradient_pages_returns_cached_value():
    context._gradient_pages.set([1, 2, 3])  # noqa: SLF001
    assert context.get_gradient_pages() == [1, 2, 3]


def test_get_biblio_pages_sets_and_returns_titles():
    mock_model = mock.Mock()
    mock_obj1 = mock.Mock()
    mock_obj1.id = 1
    mock_obj1.short_title = 'Short'
    mock_obj1.title = 'Title1'
    mock_obj2 = mock.Mock()
    mock_obj2.id = 2
    mock_obj2.short_title = ''
    mock_obj2.title = 'Title2'
    mock_model.objects.all.return_value = [mock_obj1, mock_obj2]

    with mock.patch('app.context.apps.get_model', return_value=mock_model):
        result = context.get_biblio_pages()
        assert result == [(1, 'Short'), (2, 'Title2')]
        # Should return cached value on second call
        assert context.get_biblio_pages() == [(1, 'Short'), (2, 'Title2')]


def test_get_biblio_pages_returns_cached_value():
    context._biblio_pages.set([(1, 'A'), (2, 'B')])  # noqa: SLF001
    assert context.get_biblio_pages() == [(1, 'A'), (2, 'B')]


def test_get_current_username_returns_username():
    mock_user = mock.Mock()
    mock_user.username = 'testuser'
    with mock.patch('app.context.get_current_user', return_value=mock_user):
        assert context.get_current_username() == 'testuser'
