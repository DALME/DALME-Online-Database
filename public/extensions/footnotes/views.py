"""Views for footnotes."""

from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.admin.views import chooser

from django.views.generic.edit import BaseFormView, ModelFormMixin

from .forms import FootnoteForm
from .models import Footnote


class FootnoteChooser(BaseFormView, ModelFormMixin):
    template_name = 'footnote_chooser_modal.html'
    model = Footnote
    form_class = FootnoteForm
    prefix = 'footnote'

    @property
    def edit_mode(self):
        return hasattr(self, 'object')

    def get_object(self, pk):
        if pk:
            queryset = Footnote.objects.filter(pk=pk)
            if queryset.exists() and queryset.count() == 1:
                return queryset.get()
        return None

    def get(self, _request):
        if self.request.GET.get('pk'):
            self.object = self.get_object(self.request.GET.get('pk'))

        return self.render_to_response(
            html_template=self.template_name,
            template_vars=self.get_template_vars(),
            json_data={'step': 'enter_footnote'},
        )

    def post(self, _request, pk=None):
        self.object = self.get_object(pk)
        html_template = self.template_name
        template_vars = self.get_template_vars()
        json_data = {'step': 'enter_footnote'}
        form = self.get_form()
        if form.is_valid():
            self.object = form.save(edit_mode=self.edit_mode)
            html_template = None
            template_vars = None
            result = {
                'id': form.cleaned_data['id'],
                'text': form.cleaned_data['text'],
            }

            if form.cleaned_data.get('page'):
                result['page'] = form.cleaned_data['page'].id

            json_data = {
                'step': 'footnote_entered',
                'result': result,
            }
        else:
            json_data['error'] = form.errors.as_json()

        return self.render_to_response(
            html_template=html_template,
            template_vars=template_vars,
            json_data=json_data,
        )

    def get_initial(self):
        if not self.edit_mode:
            return {'id': self.request.GET.get('id', '')}
        return None

    def get_template_vars(self):
        return chooser.shared_context(
            self.request,
            {
                'form': self.get_form(),
                'title': 'Edit Footnote' if self.edit_mode else 'New Footnote',
            },
        )

    def render_to_response(self, html_template, template_vars, json_data):
        return render_modal_workflow(
            request=self.request,
            html_template=html_template,
            template_vars=template_vars,
            json_data=json_data,
        )
