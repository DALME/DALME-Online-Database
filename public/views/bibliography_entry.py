"""View for bibliography modal."""

from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.admin.views import chooser

from django.conf import settings

from public.forms import BibliographyLinkChooserForm


def biblio_entry(request):
    initial_data = {
        'id': request.GET.get('id', ''),
        'link_text': request.GET.get('link_text', ''),
    }

    if request.method == 'POST':
        form = BibliographyLinkChooserForm(
            request.POST,
            initial=initial_data,
            prefix='bibliography-chooser',
        )

        if form.is_valid():
            result = {
                'id': form.cleaned_data['id'],
                'parentId': 'biblio_entry',
                'url': f'{settings.PUBLIC_URL}/project/bibliography/#{form.cleaned_data["id"]}/',
                'title': form.cleaned_data['link_text'].strip() or form.cleaned_data['id'],
                'prefer_this_title_as_link_text': ('link_text' in form.changed_data),
            }
            return render_modal_workflow(
                request,
                None,
                None,
                None,
                json_data={'step': 'biblio_chosen', 'result': result},
            )
    else:
        form = BibliographyLinkChooserForm(
            initial=initial_data,
            prefix='bibliography-chooser',
        )

    return render_modal_workflow(
        request,
        'wagtailadmin/chooser/bibliographic_link.html',
        None,
        chooser.shared_context(request, {'form': form}),
        json_data={'step': 'biblio_entry'},
    )
