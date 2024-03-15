"""View for footnote modal."""

from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.admin.views import chooser

from public.forms import (
    FootnoteChooserForm,
)


def enter_footnote(request):
    initial_data = {
        'note_id': request.GET.get('note_id', ''),
        'text': request.GET.get('text', ''),
    }
    title = 'Update footnote' if request.GET.get('mode', '') == 'edit' else 'Insert footnote'

    if request.method == 'POST':
        form = FootnoteChooserForm(request.POST, initial=initial_data, prefix='footnote')

        if form.is_valid():
            result = {
                'note_id': form.cleaned_data['note_id'],
                'text': form.cleaned_data['text'],
            }
            return render_modal_workflow(
                request,
                None,
                None,
                None,
                json_data={'step': 'footnote_entered', 'result': result},
            )
    else:
        form = FootnoteChooserForm(initial=initial_data, prefix='footnote')

    return render_modal_workflow(
        request,
        'wagtailadmin/chooser/footnote_entry.html',
        None,  # js template
        chooser.shared_context(
            request,
            {
                'form': form,
                'title': title,
            },
        ),
        json_data={'step': 'enter_footnote'},
    )
