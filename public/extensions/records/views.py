"""View for records extension."""

from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.admin.views import chooser
from wagtail.admin.views.generic.chooser import ChooseResultsView
from wagtail.admin.viewsets.chooser import ChooserViewSet

from django.db.models import Q
from django.views.generic.edit import BaseFormView

from ida.models import Collection, Record

from .forms import SavedSearchChooserForm


class RecordChooseResultsView(ChooseResultsView):
    def get_object_list(self):
        return self.model.objects.filter(workflow__is_public=True)

    def filter_object_list(self, objects):
        query = self.request.GET.get('q')
        if query:
            objects = objects.filter(Q(name__icontains=query) | Q(short_name__icontains=query))
        return objects


class RecordChooserViewSet(ChooserViewSet):
    model = Record
    name = 'record_chooser'
    icon = 'file-lines'
    choose_one_text = 'Choose a record'
    ordering = 'name'
    url_filter_parameters = ['q']
    preserve_url_parameters = ['multiple', 'q']
    choose_results_view_class = RecordChooseResultsView


class CollectionChooseResultsView(ChooseResultsView):
    def get_object_list(self):
        return self.model.objects.filter(is_published=True)

    def filter_object_list(self, objects):
        query = self.request.GET.get('q')
        if query:
            objects = objects.filter(name__icontains=query)
        return objects


class CollectionChooserViewSet(ChooserViewSet):
    model = Collection
    name = 'collection_chooser'
    icon = 'layer-group'
    choose_one_text = 'Choose a collection'
    ordering = 'name'
    url_filter_parameters = ['q']
    preserve_url_parameters = ['multiple', 'q']
    choose_results_view_class = CollectionChooseResultsView


class SavedSearchChooser(BaseFormView):
    template_name = 'saved_search_chooser_modal.html'
    form_class = SavedSearchChooserForm
    prefix = 'saved_search'

    def post(self, _request):
        return self.render_to_response(None)

    def get_initial(self):
        return {
            'id': self.request.GET.get('id', ''),
            'name': self.request.GET.get('name', ''),
        }

    def get_template(self, form):
        return None if form.is_valid() else self.template_name

    def get_template_vars(self, form):
        return None if form.is_valid() else chooser.shared_context(self.request, {'form': form})

    def get_json_data(self, form):
        json_data = {'step': 'saved_search_chosen' if form.is_valid() else 'enter_saved_search'}
        if form.is_valid():
            json_data.update(
                {
                    'result': {
                        'id': form.cleaned_data['id'],
                        'name': form.cleaned_data['name'],
                    }
                }
            )
        return json_data

    def render_to_response(self, _context):
        form = self.get_form()
        return render_modal_workflow(
            request=self.request,
            html_template=self.get_template(form),
            template_vars=self.get_template_vars(form),
            json_data=self.get_json_data(form),
        )
