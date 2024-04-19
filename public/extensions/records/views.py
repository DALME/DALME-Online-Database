"""View for records extension."""

from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.admin.views import chooser
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.admin.widgets import BaseChooser

from django.views.generic.edit import BaseFormView

from ida.models import Record

from .forms import SavedSearchChooserForm


class AdminRecordChooser(BaseChooser):
    model = Record
    chooser_modal_url_name = 'record_chooser:choose'
    template_name = 'record_chooser.html'


#     js_constructor = 'RecordChooser'

#     # def get_value_data_from_instance(self, instance):
#     #     return {
#     #         'id': instance.pk,
#     #         'edit_url': AdminURLFinder().get_edit_url(instance),
#     #         self.display_title_key: self.get_display_title(instance),
#     #         'gradient': instance.gradient_as_html(),
#     #         'description': instance.description,
#     #     }

#     def get_context(self, name, value_data, attrs):
#         original_field_html = self.render_hidden_input(name, value_data.get('id'), attrs)
#         return {
#             'widget': self,
#             'original_field_html': original_field_html,
#             'attrs': attrs,
#             'value': bool(value_data),
#             'edit_url': value_data.get('edit_url', ''),
#             'display_title': value_data.get(self.display_title_key, ''),
#             'gradient': value_data.get('gradient'),
#             'description': value_data.get('description'),
#             'chooser_url': self.get_chooser_modal_url(),
#             'icon': self.icon,
#             'classname': self.classname,
#         }

# @cached_property
# def media(self):
#     base_media = super().media
#     return forms.Media(
#         js=[
#             *base_media._js,
#             'wagtailadmin/js/chooser-modal.js',
#             'js/gradient-chooser-modal.js',
#         ]
#     )


class RecordChooserViewSet(ChooserViewSet):
    model = Record
    name = 'record_chooser'
    icon = 'file-lines'
    choose_one_text = 'Choose a record'
    # base_widget_class = AdminRecordChooser
    # choose_view_class = GradientChooseView
    # chosen_view_class = GradientChosenView

    def get_object_list(self):
        queryset = Record.objects.filter(type=13, workflow__is_public=True).order_by('name')
        if self.request.GET.get('search'):
            queryset = queryset.filter(name__icontains=self.request.GET['search'])
        return queryset


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
