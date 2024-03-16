"""Interface for the public.templatetags module."""


def get_names_as_string(names):
    return (
        f'{names[0]}'
        if len(names) == 1
        else f'{names[0]} and {names[1]}'
        if len(names) == 2  # noqa: PLR2004
        else f'{", ".join(names[:-1])}, and {names[-1]}'
    )
