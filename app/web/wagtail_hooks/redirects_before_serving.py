"""Add redirects before serving pages."""

from django.shortcuts import redirect


def add_redirects_before_serving_pages(page, request, serve_args, serve_kwargs):
    if page.is_root():
        home = page.get_children().live().first()
        return redirect(home.get_url(request), permanent=False)

    if page._meta.label == 'web.Section':  # noqa: SLF001
        child = page.get_children().live().first()
        if child:
            return redirect(child.get_url(request), permanent=False)
        return add_redirects_before_serving_pages(
            page.get_ancestors().last(), request, serve_args, serve_kwargs
        )  # redirect to the homepage

    return None
