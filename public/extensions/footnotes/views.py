"""Views for footnotes."""

from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.admin.views import chooser

from django.utils.functional import cached_property
from django.views.generic.edit import BaseFormView

from .forms import FootnoteChooserForm


class FootnoteChooser(BaseFormView):
    template_name = 'footnote_chooser_modal.html'
    form_class = FootnoteChooserForm
    prefix = 'footnote'

    @cached_property
    def in_edit_mode(self):
        return self.request.GET.get('mode') == 'edit'

    def get(self, _request):
        return self.render_to_response(
            html_template=self.template_name,
            template_vars=self.get_template_vars(),
            json_data={'step': 'enter_footnote'},
        )

    def post(self, _request):
        html_template = self.template_name
        template_vars = self.get_template_vars()
        json_data = {'step': 'enter_footnote'}
        form = self.get_form()
        if form.is_valid():
            form.save()
            html_template = None
            template_vars = None
            json_data = {
                'step': 'footnote_entered',
                'result': {
                    'id': form.cleaned_data['id'],
                    'page': form.cleaned_data['page'].id,
                    'text': form.cleaned_data['text'],
                },
            }

        return self.render_to_response(
            html_template=html_template,
            template_vars=template_vars,
            json_data=json_data,
        )

    def get_initial(self):
        return {
            'id': self.request.GET.get('id', ''),
            'page': self.request.GET.get('page', ''),
            'text': self.request.GET.get('text', ''),
        }

    def get_template_vars(self):
        return chooser.shared_context(
            self.request,
            {
                'form': self.get_form(),
                'title': 'Update footnote' if self.in_edit_mode else 'Insert footnote',
            },
        )

    def render_to_response(self, html_template, template_vars, json_data):
        return render_modal_workflow(
            request=self.request,
            html_template=html_template,
            template_vars=template_vars,
            json_data=json_data,
        )
