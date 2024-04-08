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
    add_to_settings_menu = True
    list_display = ['zotero_id', 'label', 'has_biblio_sources', UpdatedAtColumn()]
    chooser_viewset_class = BiblioChooserViewSet

    panels = [
        FieldRowPanel(
            [
                FieldPanel('zotero_id'),
                FieldPanel('has_biblio_sources'),
            ],
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


# def reference(request):
#     initial_data = {
#         'id': request.GET.get('id', ''),
#         'link_text': request.GET.get('link_text', ''),
#     }

#     if request.method == 'POST':
#         form = ReferenceLinkChooserForm(
#             request.POST,
#             initial=initial_data,
#             prefix='reference-chooser',
#         )

#         if form.is_valid():
#             result = {
#                 'id': form.cleaned_data['id'],
#                 'parentId': 'reference',
#                 'url': f'{settings.PUBLIC_URL}/project/bibliography/#{form.cleaned_data["id"]}/',
#                 'title': form.cleaned_data['link_text'].strip() or form.cleaned_data['id'],
#                 'prefer_this_title_as_link_text': ('link_text' in form.changed_data),
#             }
#             return render_modal_workflow(
#                 request,
#                 None,
#                 None,
#                 None,
#                 json_data={'step': 'reference_chosen', 'result': result},
#             )
#     else:
#         form = ReferenceLinkChooserForm(
#             initial=initial_data,
#             prefix='reference-chooser',
#         )

#     return render_modal_workflow(
#         request,
#         'wagtailadmin/chooser/reference.html',
#         None,
#         chooser.shared_context(request, {'form': form}),
#         json_data={'step': 'reference'},
#     )

# class ReferenceQuerySet(APIQuerySet):
#     pk_field_name = 'id'
#     pagination_style = 'offset-limit'
#     limit_query_param = 'limit'
#     offset_query_param = 'start'
#     ordering_query_param = 'sort'

#     @cached_property
#     def filter_field_aliases(self):
#         return {'pk': self.pk_field_name}

#     @cached_property
#     def get_library_instances(self):
#         tenant = get_current_tenant()
#         zotero_library_id = tenant.project.zotero_library_id
#         zotero_api_key = tenant.project.zotero_api_key
#         source_collection = tenant.project.zoter_collections.filter(has_biblio_sources=True).first().zotero_id
#         queryset_generator = zotero.Zotero(zotero_library_id, 'group', zotero_api_key)
#         return (queryset_generator, source_collection)

#     def get_filters_as_query_dict(self):
#         params = {}
#         search_terms = []
#         for key, val in self.filters:
#             # map key to the real API field name, if present in filter_field_aliases
#             key = self.filter_field_aliases.get(key, key)
#             if key != self.pk_field_name:
#                 search_terms.append(val)
#             else:
#                 params[key] = val

#         if search_terms:
#             # we only ever pass q as filter for search
#             params['q'] = ' '.join(search_terms)

#         return params

#     def run_query(self):
#         queryset_generator, source_collection = self.get_library_instances
#         params = self.get_filters_as_query_dict()

#         if list(params.keys()) == [self.pk_field_name]:
#             # if the only filter is the pk, we return the single instance
#             yield queryset_generator.item(params[self.pk_field_name], content='csljson')[0]
#             return

#         if self.ordering and self.ordering[0] != 'pk':
#             params[self.ordering_query_param] = ','.join(self.ordering)

#         if self.limit:
#             params.update({self.offset_query_param: self.offset, self.limit_query_param: self.limit})

#         params['content'] = 'csljson'
#         response_json = queryset_generator.collection_items_top(source_collection, **params)
#         for entry in response_json:
#             entry['id'] = entry['id'].split('/')[1]
#             yield entry

#     def run_count(self):
#         params = self.get_filters_as_query_dict()
#         params[self.limit_query_param] = 1
#         queryset_generator, source_collection = self.get_library_instances
#         queryset = queryset_generator.collection_items_top(source_collection, **params)
#         return len(queryset)


# class ReferenceModel(VirtualModel):
#     base_query_class = ReferenceQuerySet
#     pk_field_name = 'id'
#     pagination_style = 'offset-limit'
#     verbose_name_plural = 'references'

#     def json(self):
#         return self


# class ReferenceTitle(TitleColumn):
#     cell_template_name = 'wagtailadmin/tables/reference_title.html'

#     def get_value(self, instance):
#         return json.dumps(instance)

#     def get_cell_context_data(self, instance, parent_context):
#         context = super().get_cell_context_data(instance, parent_context)
#         context['link_id'] = instance['id']
#         return context


# class ReferenceChooseView(ChooseView):
#     @property
#     def columns(self):
#         return [
#             ReferenceTitle(
#                 'reference_json',
#                 label='Reference',
#                 get_url=(
#                     lambda obj: self.append_preserved_url_parameters(
#                         reverse(self.chosen_url_name, args=(quote(obj['id']),))
#                     )
#                 ),
#                 link_attrs={'data-chooser-modal-choice': True},
#             )
#         ]


# class ReferenceChosenResponseMixin(ChosenResponseMixin):
#     def get_object_id(self, instance):
#         return instance['id']


# class ReferenceChosenView(ChosenViewMixin, ReferenceChosenResponseMixin, View):
#     pass


# class ReferenceChooserViewSet(ChooserViewSet):
#     model = ReferenceModel
#     name = 'reference_chooser'
#     icon = 'draft'
#     choose_one_text = 'Choose a reference'
#     choose_view_class = ReferenceChooseView
#     chosen_view_class = ReferenceChosenView
#     search_tab_label = 'Search'


# reference_chooser_viewset = ReferenceChooserViewSet('reference_chooser')
