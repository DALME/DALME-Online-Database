"""Returns a custom avatar image URL instead of the default Wagtail one."""


def get_avatar(user, size=None):  # noqa: ARG001
    return user.avatar_url
