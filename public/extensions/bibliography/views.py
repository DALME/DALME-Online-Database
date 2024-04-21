"""Views for bibliography."""

from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.admin.panels import FieldPanel, FieldRowPanel
from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.admin.views import chooser
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.admin.viewsets.model import ModelViewSet

from django.views.generic.edit import BaseFormView

from ida.context import get_biblio_pages
from ida.models import ZoteroCollection

from .forms import ReferenceChooserForm


class BiblioChooserViewSet(ChooserViewSet):
    model = ZoteroCollection
    name = 'biblio_chooser'
    icon = 'book'
    choose_one_text = 'Choose a bibliographic collection'

    def get_block_class(self, name=None, module_path=None):
        meta = type(
            'Meta',
            (self.base_block_class._meta_class,),  # noqa: SLF001
            {
                'icon': self.icon,
                'template': 'bibliography_block.html',
            },
        )
        cls = type(
            name,
            (self.base_block_class,),
            {
                'target_model': self.model,
                'widget': self.widget_class(),
                'Meta': meta,
            },
        )
        cls.__module__ = module_path
        return cls


class BiblioViewSet(ModelViewSet):
    model = ZoteroCollection
    add_to_reference_index = False
    icon = 'book'
    menu_label = 'Zotero Collections'
    menu_name = 'biblio'
    menu_order = 900
    add_to_admin_menu = True
    list_display = ['id', 'label', 'has_biblio_sources', UpdatedAtColumn()]
    chooser_viewset_class = BiblioChooserViewSet

    panels = [
        FieldRowPanel(
            [
                FieldPanel('id'),
                FieldPanel('has_biblio_sources'),
            ],
            classname='field-row-panel',
        ),
        FieldPanel('label'),
    ]


biblio_chooser_viewset = BiblioChooserViewSet('biblio_chooser')


class ReferenceChooser(BaseFormView):
    template_name = 'reference_chooser_modal.html'
    form_class = ReferenceChooserForm
    prefix = 'reference'

    def post(self, _request):
        return self.render_to_response(None)

    def get_form(self):
        form = super().get_form()
        form.fields['biblio'].choices = get_biblio_pages()
        return form

    def get_initial(self):
        return {
            'id': self.request.GET.get('id', ''),
            'biblio': self.request.GET.get('biblio', ''),
            'reference': self.request.GET.get('reference', ''),
        }

    def get_template(self, form):
        return None if form.is_valid() else self.template_name

    def get_template_vars(self, form):
        return None if form.is_valid() else chooser.shared_context(self.request, {'form': form})

    def get_json_data(self, form):
        json_data = {'step': 'reference_chosen' if form.is_valid() else 'enter_reference'}
        if form.is_valid():
            json_data.update(
                {
                    'result': {
                        'id': form.cleaned_data['id'],
                        'biblio': form.cleaned_data['biblio'],
                        'reference': form.cleaned_data['reference'],
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
