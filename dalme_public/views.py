"""Define views for dalme_public."""
import urllib

from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.admin.views import chooser

from django.http import HttpResponseRedirect
from django.urls import reverse

from dalme_public.forms import (
    BibliographyLinkChooserForm,
    FootnoteChooserForm,
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
                'url': 'https://dalme.org/project/bibliography/#' + form.cleaned_data['id'] + '/',
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


def reroute_chooser(request, route=None):
    params = urllib.parse.urlencode(request.GET)

    if route:
        if str(route).isdigit():
            rev = reverse('wagtailadmin_choose_page_child', args=[route])
        elif route == 'saved_search':
            rev = reverse('wagtailadmin_choose_page_saved_search')
        elif route == 'biblio_entry':
            rev = reverse('wagtailadmin_choose_bibliography')
    else:
        rev = reverse('wagtailadmin_choose_page')

    if params:
        rev = f'{rev}?{params}'

    return HttpResponseRedirect(rev)


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
