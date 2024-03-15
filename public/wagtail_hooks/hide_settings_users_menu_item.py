"""Hide user menu item in settings."""

from wagtail import hooks


@hooks.register('construct_settings_menu')
def hide_settings_users_menu_item(request, menu_items):  # noqa: ARG001
    menu_items[:] = [item for item in menu_items if item.name not in ['users', 'groups']]
