"""Add redirects before serving pages."""

from django.shortcuts import redirect


def add_redirects_before_serving_pages(page, request, serve_args, serve_kwargs):  # noqa: ARG001
    if page.is_root():
        home = page.get_children().live().first()
        return redirect(home.url, permanent=False)

    if page._meta.label == 'public.Section':  # noqa: SLF001
        child = page.get_children().live().first()
        if child:
            return redirect(child.url, permanent=False)
        return redirect(page.get_ancestors().last().url, permanent=False)  # redirect to the homepage

    return None
