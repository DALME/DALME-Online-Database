from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from dalme_app.utils import DALMEMenus as dm
from dalme_app.models import Content_class, Content_type
from ._common import DALMEListView, get_page_chain


@method_decorator(login_required, name='dispatch')
class ModelLists(DALMEListView):
    template_name = 'dalme_app/models.html'
    dt_editor_options = {'idSrc': '"id"'}
    dt_options = {
        'serverSide': 'true',
        'responsive': 'true',
        'dom': '\'<"sub-card-header-embed d-flex"B<"#fieldsets.btn-group mr-auto"><"btn-group"f>r><"card-body"t><"sub-card-footer"i>\'',
        'stateSave': 'true',
        'select': {'style': 'multi'},
        'scrollResize': 'true',
        'scrollY': '"50vh"',
        'scrollX': '"100%"',
        'deferRender': 'true',
        'scroller': 'true',
        'processing': 'true',
        'language': {
            'searchPlaceholder': 'Search',
            'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
            },
        'rowId': '"id"',
    }
    dt_buttons = [{'extend': 'colvis', 'text': '<i class="fa fa-columns fa-fw"></i>'}]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = self.get_breadcrumb()
        sidebar_toggle = self.request.user.preferences['interface__sidebar_collapsed']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = self.get_page_title('')
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        model = self.kwargs['model']
        context['model'] = model
        if model == 'content-types':
            qs = Content_class.objects.all().order_by('name')
            parent_class_opt = {i.id: i.name for i in qs}
            context['parent_class'] = {
                'name': 'content class',
                'options': parent_class_opt
            }
        elif model == 'attribute-types':
            qs = Content_type.objects.all().order_by('name')
            parent_class_opt = {i.id: i.name for i in qs}
            context['parent_class'] = {
                'name': 'content type',
                'options': parent_class_opt
            }
        list_name = self.get_list_name()
        _list = self.get_list(list_name)
        fields_dict = self.get_fields_dict(_list)
        context['dt_options'] = self.get_dt_options(_list, fields_dict)
        context['dt_editor'] = self.get_dt_editor(_list, fields_dict)
        context['helpers'] = self.get_helpers(_list)
        return context

    def get_list_name(self, *args, **kwargs):
        return self.kwargs['model']

    def get_breadcrumb(self, *args, **kwargs):
        return [('Data Models', ''), (self.kwargs['model'].replace('_', ' ').title(), '/models/'+self.kwargs['model'])]

    def get_page_title(self, _list, *args, **kwargs):
        model = self.kwargs['model']
        if model == 'content-types':
            page_title = 'Content classes and types'
        elif model == 'attribute-types':
            page_title = 'Content types and attributes'
        return page_title

    def get_dt_fields(self, _list, *args, **kwargs):
        model = self.kwargs['model']
        if model == 'content-types':
            dt_field_list = ['id', 'name', 'short_name', 'content_class', 'description', 'attribute_types', 'has_pages', 'parents']
        elif model == 'attribute-types':
            dt_field_list = ['id', 'name', 'short_name', 'description', 'data_type', 'source', 'same_as',
                             'options_list', 'required']
        return dt_field_list

    def get_dte_fields(self, _list, *args, **kwargs):
        model = self.kwargs['model']
        if model == 'content-types':
            dte_fields = ['name', 'short_name', 'content_class', 'description', 'attribute_types', 'parents', 'r1_inheritance', 'r2_inheritance', 'has_pages', 'has_inventory']
        elif model == 'attribute-types':
            dte_fields = ['name', 'short_name', 'description', 'data_type', 'source', 'same_as', 'options_list', 'required']
        else:
            dte_fields = None
        return dte_fields

    def get_dte_buttons(self, *args, **kwargs):
        return [
            {'extend': 'create', 'text': '<i class="fa fa-plus fa-fw dt_menu_icon"></i> Create New'},
            {'extend': 'edit', 'text': '<i class="fa fa-pen fa-sm dt_menu_icon"></i> Edit Selected'},
            {'action': 'toggle_inline_edit()', 'text': '<i class="fa fa-edit fa-fw dt_menu_icon"></i> Edit Inline',
                'className': "inline-edit-toggle"},
            {'extend': 'remove', 'text': '<i class="fa fa-times fa-fw dt_menu_icon"></i> Delete Selected'},
            {'extend': 'selectNone', 'text': '<i class="fa fa-broom fa-fw dt_menu_icon"></i> Clear Selection'},
            ]
