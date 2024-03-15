"""Add redirects before serving pages."""

from wagtail import hooks

from django.shortcuts import redirect


@hooks.register('before_serve_page')
def add_redirects_before_serving_pages(page, request, serve_args, serve_kwargs):  # noqa: ARG001
    if page.is_root():
        home = page.get_children().live().first()
        return redirect(home.url, permanent=False)

    if page._meta.label == 'public.Section':  # noqa: SLF001
        url = page.get_children().live().first().url
        return redirect(url, permanent=False)

    return None
