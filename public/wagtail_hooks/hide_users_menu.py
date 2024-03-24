"""Hide user menu item in settings."""


def hide_users_menu(request, menu_items):  # noqa: ARG001
    menu_items[:] = [item for item in menu_items if item.name not in ['users', 'groups']]
