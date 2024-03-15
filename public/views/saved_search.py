"""View for saved search modal."""

from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.admin.views import chooser

from public.forms import (
    SavedSearchLinkChooserForm,
)


def saved_search(request):
    initial_data = {
        'link_text': request.GET.get('link_text', ''),
        'id': request.GET.get('id', ''),
    }

    if request.method == 'POST':
        form = SavedSearchLinkChooserForm(
            request.POST,
            initial=initial_data,
            prefix='saved-search-chooser',
        )

        if form.is_valid():
            result = {
                'id': form.cleaned_data['id'],
                'parentId': 'saved_search',
                'url': '/collections/search/' + form.cleaned_data['id'] + '/',
                'title': form.cleaned_data['link_text'].strip() or form.cleaned_data['id'],
                'prefer_this_title_as_link_text': ('link_text' in form.changed_data),
            }
            return render_modal_workflow(
                request,
                None,
                None,
                None,
                json_data={'step': 'saved_search_chosen', 'result': result},
            )
    else:
        form = SavedSearchLinkChooserForm(
            initial=initial_data,
            prefix='saved-search-chooser',
        )

    return render_modal_workflow(
        request,
        'wagtailadmin/chooser/saved_search_link.html',
        None,
        chooser.shared_context(request, {'form': form}),
        json_data={'step': 'saved_search'},
    )
