from django.contrib.auth.models import User, Group
import json
import mimetypes
import os
import urllib
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from dalme_app import functions, custom_scripts
from dalme_app.models import (Profile, Content_class, Content_type, DT_list, DT_fields, Page,
                              Source, Set, TaskList, Task, rs_resource, rs_collection_resource,
                              rs_resource_data, rs_resource_type_field, rs_user, wiki_user_groups, LanguageReference,
                              Attribute_type, CountryReference, rs_collection, Ticket, Workflow, RightsPolicy)
from haystack.generic_views import SearchView
import urllib.parse as urlparse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.conf import settings


def SessionUpdate(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])
    if request.POST['var'] == 'sidebar_toggle':
        if request.session['sidebar_toggle'] == '':
            request.session['sidebar_toggle'] = 'toggled'
        else:
            request.session['sidebar_toggle'] = ''
    return HttpResponse('ok')


def HealthCheck(request):
    return HttpResponse(status=200)


def DownloadAttachment(request, path):
    path_tokens = path.split('/')
    original_filename = path_tokens.pop(-1)
    file_path = settings.MEDIA_URL + path
    with urllib.request.urlopen(file_path) as fp:
        response = HttpResponse(fp.read())
    type, encoding = mimetypes.guess_type(original_filename)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    # response['Content-Length'] = str(os.stat(file_path).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding
    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        # filename_header = 'filename=%s' % original_filename.encode('utf-8')
        filename_header = 'filename=%s' % original_filename
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(original_filename.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response


@method_decorator(login_required, name='dispatch')
class DefaultSearch(SearchView):
    """ Default search view for Haystack"""
    template_name = 'dalme_app/search.html'
    results_per_page = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Search', ''), ('Search Results', '')]
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context = functions.set_menus(self.request, context, state)
        page_title = 'Search Results'
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        return context


@method_decorator(login_required, name='dispatch')
class DTListView(TemplateView):
    """ Generic list view that feeds Datatables """
    template_name = 'dalme_app/dtlistview.html'
    breadcrumb = []
    dt_options = {
        'pageLength': 25,
        'paging': 'true',
        'responsive': 'true',
        'fixedHeader': 'true',
        'dom': '\'<"card-table-header"B<"btn-group ml-auto"f>r><"#filters-container.collapse"><"panel-container"<"panel-left"t>><"sub-card-footer"ip>\'',
        'serverSide': 'true',
        'stateSave': 'true',
        'select': {'style': 'single'},
        'deferRender': 'true',
        'rowId': '"id"',
        'processing': 'true',
        'language': {
            'searchPlaceholder': 'Search',
            'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
            }
        }
    dt_buttons = [
        {'extend': 'colvis', 'text': '<i class="fa fa-columns fa-fw"></i>'},
        {'extend': "pageLength"}
    ]
    dte_field_list = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = self.get_breadcrumb()
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context = functions.set_menus(self.request, context, state)
        list_name = self.get_list_name()
        _list = self.get_list(list_name)
        fields_dict = self.get_fields_dict(_list)
        page_title = self.get_page_title(_list)
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        context['dt_options'] = self.get_dt_options(_list, fields_dict)
        context['dt_editor'] = self.get_dt_editor(_list, fields_dict)
        context['filters'] = self.get_filters(fields_dict)
        context['helpers'] = self.get_helpers(_list)
        context['modules'] = self.get_modules()
        return context

    def get_list_name(self, *args, **kwargs):
        if hasattr(self, 'list_name'):
            list_name = self.list_name
        else:
            list_name = None
        return list_name

    def get_list(self, list_name, *args, **kwargs):
        _list = get_object_or_404(DT_list, short_name=list_name)
        return _list

    def get_fields_dict(self, _list, *args, **kwargs):
        fields = ['field__short_name', 'field__name', 'orderable', 'visible', 'searchable', 'render_exp', 'dte_type', 'dte_options',
                  'dte_message', 'dt_class_name', 'dt_width', 'dt_name', 'dte_name', 'dte_opts', 'is_filter', 'filter_options',
                  'filter_type', 'filter_lookup', 'order']
        qset = DT_fields.objects.filter(list=_list.id).order_by('order').values(*fields)
        fields_dict = {}
        for i in qset:
            fields_dict[i['field__short_name']] = i
        return fields_dict

    def get_breadcrumb(self, *args, **kwargs):
        if hasattr(self, 'breadcrumb'):
            breadcrumb = self.breadcrumb
        else:
            breadcrumb = None
        return breadcrumb

    def get_page_title(self, _list, *args, **kwargs):
        return _list.name

    def get_dt_options(self, _list, fields_dict, *args, **kwargs):
        dt_options = {}
        options = self.dt_options
        options['ajax'] = self.get_dt_ajax_str(_list)
        dt_options['options'] = options
        dt_options['buttons'] = self.dt_buttons
        if options.get('select', {}).get('selector') is not None:
            dt_options['columnDefs'] = self.get_dt_column_defs(_list, fields_dict, sel=True)
        else:
            dt_options['columnDefs'] = self.get_dt_column_defs(_list, fields_dict)
        return dt_options

    def get_dt_ajax_str(self, _list, *args, **kwargs):
        if hasattr(_list, 'api_url'):
            base_url = _list.api_url
            dt_ajax_str = '"'+base_url+'?format=json"'
        else:
            dt_ajax_str = None
        return dt_ajax_str

    def get_dt_column_defs(self, _list, fields_dict, *args, **kwargs):
        sel = kwargs.get('sel', False)
        if sel:
            column_defs = [{'orderable': 'false', 'className': '"select-checkbox"', 'targets':   0, 'defaultContent': '""'}]
            col = 1
        else:
            column_defs = []
            col = 0
        for field, options in fields_dict.items():
            c_dict = {}
            if options.get('dt_name') is not None:
                dt_name = options['dt_name']
            else:
                dt_name = options.get('field__short_name')
            c_dict['title'] = '"'+options.get('field__name')+'"'
            c_dict['targets'] = col
            c_dict['data'] = '"'+dt_name+'"'
            if options.get('dte_name') is not None:
                c_dict['editField'] = '"'+options.get('dte_name')+'"'
            c_dict['defaultContent'] = '""'
            c_dict['visible'] = str(options.get('visible')).lower()
            c_dict['orderable'] = str(options.get('orderable')).lower()
            c_dict['searchable'] = str(options.get('searchable')).lower()
            if options.get('render_exp') is not None:
                c_dict['render'] = options.get('render_exp')
            if options.get('dt_width') is not None:
                c_dict['width'] = '"'+options.get('dt_width')+'"'
            if options.get('dt_class_name') is not None:
                c_dict['className'] = '"' + options.get('dt_class_name') + '"'
            column_defs.append(c_dict)
            col = col + 1
        return column_defs

    def get_dte_fields(self, _list, *args, **kwargs):
        if hasattr(self, 'dte_field_list'):
            dte_fields = self.dte_field_list
        else:
            dte_fields = None
        return dte_fields

    def get_dt_editor(self, _list, fields_dict, *args, **kwargs):
        if self.get_dte_fields(_list) is not None:
            dte_fields = self.get_dte_fields(_list)
            dt_editor = {}
            dt_editor['ajax_url'] = _list.api_url
            fields = []
            for f in dte_fields:
                lf = fields_dict.get(f)
                if lf is not None:
                    f_dict = {}
                    if lf.get('dte_name') is not None:
                        f_dict['name'] = lf['dte_name']
                    elif lf.get('dt_name') is not None:
                        f_dict['name'] = lf['dt_name']
                    else:
                        f_dict['name'] = lf['field__short_name']
                    f_dict['label'] = lf['field__name']
                    if lf.get('dte_type') is not None:
                        f_dict['type'] = lf['dte_type']
                    else:
                        f_dict['type'] = 'text'
                    if lf.get('dte_opts') is not None:
                        if f_dict['type'] == 'autoComplete':
                            ac_opts = eval(lf['dte_opts'])
                        else:
                            f_dict['opts'] = eval(lf['dte_opts'])
                            ac_opts = None
                    if lf.get('dte_options') is not None:
                        if f_dict['type'] == 'autoComplete':
                            if type(ac_opts) is dict:
                                ac_opts['source'] = eval(lf['dte_options'])
                            else:
                                ac_opts = {'source': eval(lf['dte_options'])}
                            f_dict['opts'] = ac_opts
                        else:
                            f_dict['options'] = eval(lf['dte_options'])
                    if lf.get('dte_message') is not None:
                        f_dict['fieldInfo'] = lf['dte_message']
                    fields.append(f_dict)
            dt_editor['fields'] = fields
            if self.get_dte_options() is not None:
                dt_editor['options'] = self.get_dte_options()
            if self.get_dte_buttons() is not None:
                dt_editor['buttons'] = self.get_dte_buttons()
        else:
            dt_editor = None
        return dt_editor

    def get_filters(self, fields_dict, *args, **kwargs):
        filters = []
        types_w_lookups = ['text', 'date', 'datetime', 'integer']
        for k, d in fields_dict.items():
            if d['is_filter']:
                filter = {}
                filter['label'] = d['field__name']
                filter['field'] = k
                if d.get('filter_type') is not None:
                    filter['type'] = d['filter_type']
                else:
                    filter['type'] = 'text'
                if d.get('filter_lookup') is not None:
                    filter['lookup'] = d['filter_lookup']
                if filter['type'] in types_w_lookups:
                    filter['lookups'] = functions.get_filter_lookups(filter['type'])
                if filter['type'] == 'check' or filter['type'] == 'select':
                    if d.get('filter_mode') is not None:
                        f_mode = d['filter_mode']
                    else:
                        f_mode = 'complete'
                    if d.get('filter_options') is not None:
                        # values = eval(dict['filter_options'])
                        values = d['filter_options']
                        filter = functions.add_filter_options(values, filter, f_mode)
                filters.append(filter)
        if filters == []:
            filters = None
        return filters

    def get_helpers(self, _list, *args, **kwargs):
        helpers = _list.helpers
        if helpers is not None and helpers != '':
            helpers = [i.strip() for i in helpers.split(',')]
        return helpers

    def get_dte_options(self, *args, **kwargs):
        if hasattr(self, 'dt_editor_options'):
            dte_options = self.dt_editor_options
        else:
            dte_options = None
        return dte_options

    def get_dte_buttons(self, *args, **kwargs):
        if hasattr(self, 'dt_editor_buttons'):
            dte_buttons = self.dt_editor_buttons
        else:
            dte_buttons = None
        return dte_buttons

    def get_modules(self, *args, **kwargs):
        if hasattr(self, 'module_list'):
            module_list = self.module_list
        else:
            module_list = None
        return module_list


@method_decorator(login_required, name='dispatch')
class ModelLists(DTListView):
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
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context = functions.set_menus(self.request, context, state)
        page_title = self.get_page_title('')
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        model = self.kwargs['model']
        context['model'] = model
        if model == 'content_types':
            qs = Content_class.objects.all().order_by('name')
            parent_class_opt = {i.id: i.name for i in qs}
            context['parent_class'] = {
                'name': 'content class',
                'options': parent_class_opt
            }
        elif model == 'attribute_types':
            qs = Content_type.objects.all().order_by('name')
            parent_class_opt = {i.id: i.name for i in qs}
            context['parent_class'] = {
                'name': 'content type',
                'options': parent_class_opt
            }
        elif model == 'dt_fields':
            context['dt_fieldsets'] = {
                'DT Fields': [3, 4, 5, 6, 7, 8, 9, 10],
                'DTE Fields': [11, 12, 13, 14, 15],
                'Filter Fields': [16, 17, 18, 19]
                }
            qs = DT_list.objects.all().order_by('name')
            parent_class_opt = {i.id: i.name for i in qs}
            context['parent_class'] = {
                'name': 'list',
                'options': parent_class_opt
            }
        list_name = self.get_list_name()
        _list = self.get_list(list_name)
        fields_dict = self.get_fields_dict(_list)
        context['dt_options'] = self.get_dt_options(_list, fields_dict)
        context['dt_editor'] = self.get_dt_editor(_list, fields_dict)
        context['helpers'] = self.get_helpers(_list)
        context['modules'] = self.get_modules()
        return context

    def get_list_name(self, *args, **kwargs):
        return self.kwargs['model']

    def get_breadcrumb(self, *args, **kwargs):
        if self.kwargs['model'] == 'dt_fields':
            breadcrumb = [('Data Models', ''), ('DataTables Fields', '/models/dt_fields')]
        else:
            breadcrumb = [('Data Models', ''), (self.kwargs['model'].replace('_', ' ').title(), '/models/'+self.kwargs['model'])]
        return breadcrumb

    def get_page_title(self, _list, *args, **kwargs):
        model = self.kwargs['model']
        if model == 'content_types':
            page_title = 'Content classes and types'
        elif model == 'attribute_types':
            page_title = 'Content types and attributes'
        elif model == 'dt_fields':
            page_title = 'DataTables lists and fields'
        return page_title

    def get_dt_fields(self, _list, *args, **kwargs):
        model = self.kwargs['model']
        if model == 'content_types':
            dt_field_list = ['id', 'name', 'short_name', 'content_class', 'description', 'attribute_types', 'has_pages', 'parents']
        elif model == 'attribute_types':
            dt_field_list = ['id', 'name', 'short_name', 'description', 'data_type', 'source', 'same_as',
                             'options_list', 'required']
        elif model == 'dt_fields':
            dt_field_list = ['id', 'list', 'field', 'order', 'dt_name', 'orderable', 'visible', 'searchable',
                             'render_exp', 'dt_class_name', 'dt_width', 'dte_name', 'dte_type', 'dte_options',
                             'dte_opts', 'dte_message', 'is_filter', 'filter_type', 'filter_mode', 'filter_options',
                             'filter_lookup']
        return dt_field_list

    def get_dte_fields(self, _list, *args, **kwargs):
        model = self.kwargs['model']
        if model == 'content_types':
            dte_fields = ['name', 'short_name', 'content_class', 'description', 'attribute_types', 'parents', 'r1_inheritance', 'r2_inheritance', 'has_pages', 'has_inventory']
        elif model == 'attribute_types':
            dte_fields = ['name', 'short_name', 'description', 'data_type', 'source', 'same_as', 'options_list', 'required']
        elif model == 'dt_fields':
            dte_fields = ['dt_name', 'order', 'orderable', 'visible', 'searchable', 'render_exp', 'dt_class_name', 'dt_width',
                          'dte_name', 'dte_type', 'dte_options', 'dte_opts', 'dte_message', 'is_filter', 'filter_type',
                          'filter_mode', 'filter_options', 'filter_lookup']
        else:
            dte_fields = None
        return dte_fields

    def get_dte_buttons(self, *args, **kwargs):
        model = self.kwargs['model']
        dte_buttons = []
        if model != 'dt_fields':
            dte_buttons.append({'extend': 'create', 'text': '<i class="fa fa-plus fa-fw dt_menu_icon"></i> Create New'})
            dte_buttons.append({'extend': 'edit', 'text': '<i class="fa fa-pen fa-sm dt_menu_icon"></i> Edit Selected'})
        dte_buttons.append({'action': 'toggle_inline_edit()', 'text': '<i class="fa fa-edit fa-fw dt_menu_icon"></i> Edit Inline',
                            'className': "inline-edit-toggle"})
        dte_buttons.append({'extend': 'remove', 'text': '<i class="fa fa-times fa-fw dt_menu_icon"></i> Delete Selected'})
        dte_buttons.append({'extend': 'selectNone', 'text': '<i class="fa fa-broom fa-fw dt_menu_icon"></i> Clear Selection'})
        return dte_buttons

    def get_modules(self, *args, **kwargs):
        model = self.kwargs['model']
        if model == 'dt_fields':
            module_list = ['fieldsets']
        else:
            module_list = None
        return module_list


@method_decorator(login_required, name='dispatch')
class SourceList(DTListView):
    """ Lists sources """
    dt_editor_options = {'idSrc': '"id"', 'template': '"#inventoryForm"'}
    dte_field_list = ['name', 'short_name', 'type', 'parent', 'has_inventory']

    def get_list_name(self, *args, **kwargs):
        list_name = 'all'
        if 'type' in self.request.GET:
            list_name = self.request.GET['type']
        return list_name

    def get_breadcrumb(self, *args, **kwargs):
        _type = self.get_list_name()
        if _type == 'all':
            breadcrumb = [('Sources', ''), ('All Sources', '/sources')]
        else:
            list_label = DT_list.objects.get(short_name=_type).name
            breadcrumb = [('Sources', ''), (list_label, '/sources?type='+_type)]
        return breadcrumb

    def get_dt_ajax_str(self, _list, *args, **kwargs):
        base_url = _list.api_url
        _type = _list.short_name
        if _type == 'sources':
            dt_ajax_str = '"'+base_url+'?format=json"'
        else:
            dt_ajax_str = '"'+base_url+'?format=json&type='+_type+'"'
        return dt_ajax_str

    def get_dt_fields(self, _list, *args, **kwargs):
        dt_fields = DT_fields.objects.filter(list=_list).values_list('field__short_name', flat=True)
        return dt_fields

    def get_modules(self, *args, **kwargs):
        module_list = None
        if 'type' in self.request.GET:
            if self.request.GET['type'] == 'records':
                module_list = ['filters']
                if functions.check_group(self.request, ['Staff']):
                    module_list.append('workflow')
        return module_list

    def get_dte_buttons(self, *args, **kwargs):
        dte_buttons = []
        if self.request.user.has_perm('dalme_app.add_source'):
            dte_buttons.append({'extend': 'create', 'text': '<i class="fa fa-plus fa-fw dt_menu_icon"></i> Create New Source', 'formTitle': 'Create New Source'})
        if self.request.user.has_perm('dalme_app.change_source'):
            dte_buttons.append({'extend': 'edit', 'text': '<i class="fa fa-pen fa-sm dt_menu_icon"></i> Edit Selected Source', 'formTitle': 'Edit Source Information'})
        if self.request.user.has_perm('dalme_app.delete_source'):
            dte_buttons.append({'extend': 'remove', 'text': '<i class="fa fa-times fa-fw dt_menu_icon"></i> Delete Selected Source', 'formTitle': 'Delete Source',
                                'formMessage': 'Are you sure you wish to remove this source from the database? This action cannot be undone.'})
        dte_buttons.append({'action': 'save_set("create")', 'text': '<i class="fa fa-folder fa-fw dt_menu_icon"></i> Create New Set'})
        dte_buttons.append({'action': 'save_set("add")', 'text': '<i class="fa fa-folder-plus fa-fw dt_menu_icon"></i> Add Sources to Set...'})
        return dte_buttons


@method_decorator(login_required, name='dispatch')
class SourceDetail(DetailView):
    model = Source

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'set' in self.request.GET:
            workset = Set.objects.get(pk=self.request.GET['set'])
            members = Source.objects.filter(sets__set_id=workset.id)
            current_index = (*members,).index(self.object)
            try:
                previous_id = str(members[current_index - 1].id)
            except (IndexError, AssertionError):
                previous_id = 'none'
            try:
                next_id = str(members[current_index + 1].id)
            except (IndexError, AssertionError):
                next_id = 'none'
            para = {
                'workset_id': str(workset.id),
                'name': workset.name,
                'description': workset.description,
                'current': current_index + 1,
                'current_id': str(self.object.id),
                'prev_id': previous_id,
                'next_id': next_id,
                'total': members.count(),
                'endpoint': workset.endpoint,
                'progress': round(workset.workset_progress, 2)
            }
            context['workset'] = para
        breadcrumb = self.get_breadcrumb()
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context = functions.set_menus(self.request, context, state)
        page_title = self.object.name
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        context['source_id'] = self.object.id
        context['comments_count'] = self.object.comments.count()
        has_inv = self.object.has_inventory
        has_pages = self.object.pages.all().exists()
        has_children = self.object.source_set.all().exists()
        has_agents = self.object.agents is not None and len(self.object.agents) > 0
        has_places = self.object.places is not None and len(self.object.places) > 0
        context['has_inv'] = has_inv
        context['has_pages'] = has_pages
        context['has_children'] = has_children
        context['has_agents'] = has_agents
        context['has_places'] = has_places
        if has_inv:
            context['workflow'] = self.object.workflow
            wf_stages = []
            for k, v in dict(Workflow.PROCESSING_STAGES).items():
                current = 0
                if k == self.object.workflow.stage:
                    current = 1
                wf_stages.append([v, getattr(self.object.workflow, v + '_done'), current])
            context['wf_stages'] = wf_stages
        source_data = {
            'Type': self.object.type.name,
            'Name': self.object.name,
            'Short name': self.object.short_name,
            'List': functions.format_boolean(has_inv),
        }
        if self.object.parent:
            source_data['Parent'] = '<a href="{}">{}</a>'.format('/sources/'+str(self.object.parent.id), self.object.parent.name)
        context['source_data'] = source_data
        context['source_metadata'] = {
            'ID': str(self.object.id),
            'Created': functions.format_rct(self.object.creation_username, self.object.creation_timestamp),
            'Modified': functions.format_rct(self.object.modification_username, self.object.modification_timestamp),
        }
        attribute_data = self.process_attributes(self.object.attributes.all().select_related('attribute_type'))
        if attribute_data.get('description', None) is not None:
            context['description'] = attribute_data['description']
        context['attribute_data'] = attribute_data['attributes']
        context['inherited_data'] = self.process_attributes(self.object.inherited.all().select_related('attribute_type'))['attributes']
        tables = []
        if has_pages:
            title = 'Pages (' + str(len(self.object.pages.all())) + ')'
            folios = functions.get_editor_folios(self.object)
            context['folio_count'] = folios['folio_count']
            context['folio_menu'] = folios['folio_menu']
            context['folio_list'] = folios['folio_list']
            tables.append(['pages', 'fa-book-open', title])
        if has_children:
            title = 'Children (' + str(len(self.object.source_set.all())) + ')'
            context['children'] = self.object.source_set.all().order_by('name')
            tables.append(['children', 'fa-sitemap', title])
        if has_agents:
            title = 'Agents (' + str(len(self.object.agents)) + ')'
            context['agents'] = self.object.agents.all().select_related('content_type')
            tables.append(['agents', 'fa-user-friends', title])
        if has_places:
            title = 'Places (' + str(len(self.object.places)) + ')'
            context['places'] = self.object.places.all().select_related('content_type')
            tables.append(['places', 'fa-map-marker-alt', title])
        if tables != []:
            context['tables'] = tables
            context['table_options'] = {
                'responsive': 'true',
                'dom': '''"<'sub-card-header d-flex'<'card-header-title'>fr><'card-body't>"''',
                'stateSave': 'true',
                'select': {'style': 'single'},
                'scrollResize': 'true',
                'scrollY': '"30vh"',
                'scrollX': '"100%"',
                'scrollCollapse': 'true',
                'deferRender': 'true',
                'scroller': 'true',
                'language': {
                    'searchPlaceholder': 'Search',
                    'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
                    },
                }
        return context

    def process_attributes(self, qset):
        result = {}
        attributes = []
        for a in qset:
            label = a.attribute_type.name
            value = functions.get_attribute_value(a)
            if label == 'Description':
                result['description'] = value
            else:
                attributes.append({'label': label, 'value': value})
        result['attributes'] = attributes
        return result

    def get_breadcrumb(self, *args, **kwargs):
        try:
            parsed_ref = urlparse.urlparse(self.request.META.get('HTTP_REFERER', '/'))
            s_type = urlparse.parse_qs(parsed_ref.query)['type'][0]
        except:
            s_type = 'all'
        if s_type == 'all':
            breadcrumb = [('Sources', ''), ('All Sources', '/sources')]
        elif s_type == 'inventories':
            breadcrumb = [('Repository', ''), ('Inventories', '/sources?type=inventories')]
        else:
            list_label = DT_list.objects.get(short_name=s_type).name
            breadcrumb = [('Sources', ''), (list_label, '/sources?type='+s_type)]
        return breadcrumb

    def get_object(self):
        """ Raise a 404 instead of exception on things that aren't proper UUIDs """
        try:
            object = super().get_object()
            return object
        except ObjectDoesNotExist:
            raise Http404


def SourceManifest(request, pk):
    context = {}
    source = Source.objects.get(pk=pk)
    context['source'] = source
    context['page_canvases'] = [page.get_canvas() for page in source.pages.all()]
    return render(request, 'dalme_app/source_manifest.html', context)


@method_decorator(login_required, name='dispatch')
class UserList(DTListView):
    """ Lists users and allows editing and creation of new records via the API """
    list_name = 'users'
    breadcrumb = [('Project', ''), ('Users', '/users')]
    dt_editor_options = {'idSrc': '"id"'}
    dte_field_list = ['first_name', 'last_name', 'full_name', 'email', 'username',
                      'password', 'is_staff', 'is_superuser', 'groups', 'dam_usergroup',
                      'wiki_groups', 'wp_role']

    def get_dte_buttons(self, *args, **kwargs):
        dte_buttons = []
        if self.request.user.has_perm('dalme_app.add_user'):
            dte_buttons.append({'extend': 'create', 'text': '<i class="fa fa-plus fa-fw dt_menu_icon"></i> Create New', 'formTitle': 'Create New User'})
        if self.request.user.has_perm('dalme_app.change_user'):
            dte_buttons.append({'extend': 'edit', 'text': '<i class="fa fa-pen fa-sm dt_menu_icon"></i> Edit Selected', 'formTitle': 'Edit User Information'})
        if self.request.user.has_perm('dalme_app.delete_user'):
            dte_buttons.append({'extend': 'remove', 'text': '<i class="fa fa-times fa-fw dt_menu_icon"></i> Delete Selected', 'formTitle': 'Delete User',
                                'formMessage': 'Are you sure you wish to remove this user from the database? This action cannot be undone.'})
        return dte_buttons


@method_decorator(login_required, name='dispatch')
class UserDetail(DetailView):
    model = Profile
    template_name = 'dalme_app/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Project', ''), ('Users', '/users')]
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context = functions.set_menus(self.request, context, state)
        page_title = self.object.full_name
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        user_data = {
            'First name': self.object.user.first_name,
            'Last name': self.object.user.last_name,
            'User Id': self.object.user.id,
            'Email': functions.format_email(self.object.user.email),
            'Staff': functions.format_boolean(self.object.user.is_staff),
            'Superuser': functions.format_boolean(self.object.user.is_superuser),
            'Active': functions.format_boolean(self.object.user.is_active),
            'Joined': functions.format_date(self.object.user.date_joined, 'timestamp-long'),
            'Last login': functions.format_date(self.object.user.last_login, 'timestamp-long'),
            'Groups': self.object.user.groups,
            'WordPress role': self.object.get_wp_role_display()
        }
        context['user_data'] = user_data
        context['image_url'] = self.object.profile_image
        return context

    def get_object(self):
        """ Raise a 404 instead of exception on things that aren't proper UUIDs"""
        try:
            object = Profile.objects.get(user__username=self.kwargs['username'])
            return object
        except ObjectDoesNotExist:
            raise Http404


@method_decorator(login_required, name='dispatch')
class AsyncTaskList(DTListView):
    breadcrumb = [('System', ''), ('Asynchronous Tasks', '/async_tasks')]
    list_name = 'async_tasks'
    dt_options = {
        'pageLength': 25,
        'paging': 'true',
        'responsive': 'true',
        'fixedHeader': 'true',
        'dom': '\'<"card-table-header"B<"btn-group ml-auto"f>r><"#filters-container.collapse.clearfix"><"panel-container"<"panel-left"t>><"sub-card-footer"ip>\'',
        'serverSide': 'true',
        'stateSave': 'true',
        'select': {'style': 'single'},
        'deferRender': 'true',
        'rowId': '"id"',
        'language': {
            'searchPlaceholder': 'Search',
            'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
            },
        'order': '[[ 0, "desc" ]]'
        }


@method_decorator(login_required, name='dispatch')
class CountryList(DTListView):
    breadcrumb = [('System', ''), ('Countries', '/countries')]
    list_name = 'countries'
    dt_editor_options = {'idSrc': '"id"'}
    dte_field_list = ['name', 'alpha_3_code', 'alpha_2_code', 'num_code']
    dt_options = {
        'pageLength': 25,
        'paging': 'true',
        'responsive': 'true',
        'fixedHeader': 'true',
        'dom': '\'<"card-table-header"B<"btn-group ml-auto"f>r><"#filters-container.collapse.clearfix"><"panel-container"<"panel-left"t>><"sub-card-footer"ip>\'',
        'serverSide': 'true',
        'stateSave': 'true',
        'select': {'style': 'single'},
        'deferRender': 'true',
        'rowId': '"id"',
        'processing': 'true',
        'language': {
            'searchPlaceholder': 'Search',
            'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
            },
        'order': '[[ 1, "asc" ]]'
        }

    def get_dte_buttons(self, *args, **kwargs):
        dte_buttons = []
        if self.request.user.has_perm('dalme_app.add_country'):
            dte_buttons.append({'extend': 'create', 'text': '<i class="fa fa-plus fa-fw dt_menu_icon"></i> Create New', 'formTitle': 'Create New Country'})
        if self.request.user.has_perm('dalme_app.change_country'):
            dte_buttons.append({'extend': 'edit', 'text': '<i class="fa fa-pen fa-sm dt_menu_icon"></i> Edit Selected', 'formTitle': 'Edit Country Information'})
        if self.request.user.has_perm('dalme_app.delete_country'):
            dte_buttons.append({'extend': 'remove', 'text': '<i class="fa fa-times fa-fw dt_menu_icon"></i> Delete Selected', 'formTitle': 'Delete Country',
                                'formMessage': 'Are you sure you wish to remove this country from the database? This action cannot be undone.'})
        return dte_buttons


@method_decorator(login_required, name='dispatch')
class CityList(DTListView):
    breadcrumb = [('System', ''), ('Cities', '/cities')]
    list_name = 'cities'
    dt_editor_options = {'idSrc': '"id"'}
    dte_field_list = ['name', 'administrative_region', 'country']
    dt_options = {
        'pageLength': 25,
        'paging': 'true',
        'responsive': 'true',
        'fixedHeader': 'true',
        'dom': '\'<"card-table-header"B<"btn-group ml-auto"f>r><"#filters-container.collapse.clearfix"><"panel-container"<"panel-left"t>><"sub-card-footer"ip>\'',
        'serverSide': 'true',
        'stateSave': 'true',
        'select': {'style': 'single'},
        'deferRender': 'true',
        'rowId': '"id"',
        'processing': 'true',
        'language': {
            'searchPlaceholder': 'Search',
            'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
            },
        'order': '[[ 1, "asc" ]]'
        }

    def get_dte_buttons(self, *args, **kwargs):
        dte_buttons = []
        if self.request.user.has_perm('dalme_app.add_cityreference'):
            dte_buttons.append({'extend': 'create', 'text': '<i class="fa fa-plus fa-fw dt_menu_icon"></i> Create New', 'formTitle': 'Create New City'})
        if self.request.user.has_perm('dalme_app.change_cityreference'):
            dte_buttons.append({'extend': 'edit', 'text': '<i class="fa fa-pen fa-sm dt_menu_icon"></i> Edit Selected', 'formTitle': 'Edit City Information'})
        if self.request.user.has_perm('dalme_app.delete_cityreference'):
            dte_buttons.append({'extend': 'remove', 'text': '<i class="fa fa-times fa-fw dt_menu_icon"></i> Delete Selected', 'formTitle': 'Delete City',
                                'formMessage': 'Are you sure you wish to remove this city from the database? This action cannot be undone.'})
        return dte_buttons


@method_decorator(login_required, name='dispatch')
class RightsList(DTListView):
    breadcrumb = [('Project', ''), ('Rights Policies', '/rights')]
    list_name = 'rights'
    dt_editor_options = {'idSrc': '"id"'}
    dte_field_list = ['name', 'rights_holder', 'rights_status', 'rights', 'notice_display', 'rights_notice', 'licence', 'attachments']
    dt_options = {
        'pageLength': 25,
        'paging': 'true',
        'responsive': 'true',
        'fixedHeader': 'true',
        'dom': '\'<"card-table-header"B<"btn-group ml-auto"f>r><"#filters-container.collapse.clearfix"><"panel-container"<"panel-left"t>><"sub-card-footer"ip>\'',
        'serverSide': 'true',
        'stateSave': 'true',
        'select': {'style': 'single'},
        'deferRender': 'true',
        'rowId': '"id"',
        'processing': 'true',
        'language': {
            'searchPlaceholder': 'Search',
            'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
            },
        'order': '[[ 1, "asc" ]]'
        }

    def get_dte_buttons(self, *args, **kwargs):
        dte_buttons = []
        if self.request.user.has_perm('dalme_app.add_rightspolicy'):
            dte_buttons.append({'extend': 'create', 'text': '<i class="fa fa-plus fa-fw dt_menu_icon"></i> Create New', 'formTitle': 'Create New Policy'})
        if self.request.user.has_perm('dalme_app.change_rightspolicy'):
            dte_buttons.append({'extend': 'edit', 'text': '<i class="fa fa-pen fa-sm dt_menu_icon"></i> Edit Selected', 'formTitle': 'Edit Policy Information'})
        if self.request.user.has_perm('dalme_app.delete_rightspolicy'):
            dte_buttons.append({'extend': 'remove', 'text': '<i class="fa fa-times fa-fw dt_menu_icon"></i> Delete Selected', 'formTitle': 'Delete Policy',
                                'formMessage': 'Are you sure you wish to remove this policy from the database? This action cannot be undone.'})
        return dte_buttons


@method_decorator(login_required, name='dispatch')
class RightsDetail(DetailView):
    model = RightsPolicy
    template_name = 'dalme_app/generic_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Project', ''), ('Rights Policies', '/rights')]
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context = functions.set_menus(self.request, context, state)
        page_title = 'Policy: ' + self.object.name
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        context['object_class'] = 'Rights Policy'
        context['object_icon'] = 'fas fa-copyright'
        if self.object.notice_display:
            notice_disp = '<i class="fas fa-check-square"></i>'
        else:
            notice_disp = '<i class="far fa-square"></i>'
        context['attribute_dictionaries'] = ['Rights Notice']
        context['object_attributes'] = {
            'ID': self.object.id,
            'Name': self.object.name,
            'Rights Holder': self.object.rights_holder,
            'Rights Status': self.object.get_rights_status_display(),
            'Rights': self.object.rights,
            'Notice Display': notice_disp,
            'Rights Notice': json.loads(self.object.rights_notice),
            'Licence': self.object.licence,
            'Attachment': self.object.attachments.filename
        }
        return context

    def get_object(self):
        """ Raise a 404 instead of exception on things that aren't proper UUIDs"""
        try:
            object = RightsPolicy.objects.get(pk=self.kwargs['pk'])
            return object
        except ObjectDoesNotExist:
            raise Http404


@method_decorator(login_required, name='dispatch')
class LanguageList(DTListView):
    breadcrumb = [('System', ''), ('Languages', '/languages')]
    list_name = 'languages'
    dt_editor_options = {'idSrc': '"id"'}
    dte_field_list = ['name', 'glottocode', 'iso6393', 'parent', 'type']
    dt_options = {
        'pageLength': 25,
        'paging': 'true',
        'responsive': 'true',
        'fixedHeader': 'true',
        'dom': '\'<"card-table-header"B<"btn-group ml-auto"f>r><"#filters-container.collapse.clearfix"><"panel-container"<"panel-left"t>><"sub-card-footer"ip>\'',
        'serverSide': 'true',
        'stateSave': 'true',
        'select': {'style': 'single'},
        'deferRender': 'true',
        'rowId': '"id"',
        'processing': 'true',
        'language': {
            'searchPlaceholder': 'Search',
            'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
            }
        }

    def get_dte_buttons(self, *args, **kwargs):
        dte_buttons = []
        if self.request.user.has_perm('dalme_app.add_language'):
            dte_buttons.append({'extend': 'create', 'text': '<i class="fa fa-plus fa-fw dt_menu_icon"></i> Create New', 'formTitle': 'Create New Language'})
        if self.request.user.has_perm('dalme_app.change_language'):
            dte_buttons.append({'extend': 'edit', 'text': '<i class="fa fa-pen fa-sm dt_menu_icon"></i> Edit Selected', 'formTitle': 'Edit Language Information'})
        if self.request.user.has_perm('dalme_app.delete_language'):
            dte_buttons.append({'extend': 'remove', 'text': '<i class="fa fa-times fa-fw dt_menu_icon"></i> Delete Selected', 'formTitle': 'Delete Language',
                                'formMessage': 'Are you sure you wish to remove this language from the database? This action cannot be undone.'})
        return dte_buttons


@method_decorator(login_required, name='dispatch')
class ImageList(DTListView):
    breadcrumb = [('DAM Images', '/images')]
    list_name = 'images'
    dt_editor_options = {'idSrc': '"id"'}
    dte_field_list = ['field8', 'field79', 'field12', 'field3', 'collections']
    dt_options = {
        'pageLength': 25,
        'paging': 'true',
        'responsive': 'true',
        'fixedHeader': 'true',
        'dom': '\'<"card-table-header"B<"btn-group ml-auto"f>r><"#filters-container.collapse.clearfix"><"panel-container"<"panel-left"t>><"sub-card-footer"ip>\'',
        'serverSide': 'true',
        'stateSave': 'true',
        'select': {'style': 'multi'},
        'deferRender': 'true',
        'rowId': '"id"',
        'processing': 'true',
        'language': {
            'searchPlaceholder': 'Search',
            'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
            },
        # 'order': '[[ 1, "asc" ]]'
        }
    module_list = ['filters', 'preview']

    def get_dte_buttons(self, *args, **kwargs):
        dte_buttons = []
        if self.request.user.has_perm('dalme_app.change_rs_resource'):
            dte_buttons.append({'extend': 'edit', 'text': '<i class="fa fa-pen fa-sm dt_menu_icon"></i> Edit Selected', 'formTitle': 'Edit Image Information'})
            dte_buttons.append({'action': 'toggle_inline_edit()', 'text': '<i class="fa fa-edit fa-fw dt_menu_icon"></i> Edit Inline', 'className': "inline-edit-toggle"})
        if self.request.user.has_perm('dalme_app.delete_rs_resource'):
            dte_buttons.append({'extend': 'remove', 'text': '<i class="fa fa-times fa-fw dt_menu_icon"></i> Delete Selected', 'formTitle': 'Delete Image',
                                'formMessage': 'Are you sure you wish to remove this image from the DAM? This action cannot be undone.'})
        if self.request.user.has_perm('dalme_app.add_source'):
            dte_buttons.append({'extend': 'selectAll', 'text': '<i class="fa fa-check-double fa-fw dt_menu_icon"></i> Select All'})
            dte_buttons.append({'extend': 'selectNone', 'text': '<i class="fa fa-broom fa-fw dt_menu_icon"></i> Clear Selection'})
            dte_buttons.append({'extend': 'selected', 'action': 'create_source_from_selected()', 'text': '<i class="fa fa-plus-square fa-fw dt_menu_icon"></i> Create Source from Selection'})
        return dte_buttons


@method_decorator(login_required, name='dispatch')
class ImageDetail(DetailView):
    model = rs_resource
    template_name = 'dalme_app/image_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('DAM Images', '/images')]
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context = functions.set_menus(self.request, context, state)
        page_title = 'DAM Image ' + str(self.object.ref)
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        image_data = {
            'DAM Id': self.object.ref,
            'Created': functions.format_date(self.object.creation_date, 'timestamp'),
            'Creator': functions.format_user(self.object.created_by, 'dam', 'html'),
            'Record modified': functions.format_date(self.object.modified, 'timestamp'),
            'File modified': functions.format_date(self.object.file_modified, 'timestamp'),
            'Filesize': self.object.file_size,
            'Image?': functions.format_boolean(self.object.has_image)
        }
        context['image_data'] = image_data
        tables = []
        if rs_resource_data.objects.filter(resource=self.object.ref).order_by('resource_type_field').exists():
            attribute_data = []
            attributes = rs_resource_data.objects.filter(resource=self.object.ref).order_by('resource_type_field')
            for a in attributes:
                value = a.value
                name = a.resource_type_field.name
                label = a.resource_type_field.title
                d = {
                    'name': name,
                    'label': label,
                    'value': value,
                }
                attribute_data.append(d)
            context['attribute_data'] = attribute_data
        if rs_collection_resource.objects.filter(resource=self.object.ref).exists():
            collections = []
            col_list = rs_collection_resource.objects.filter(resource=self.object.ref)
            for col in col_list:
                path = ''
                if col.collection.theme:
                    path += col.collection.theme
                    if col.collection.theme2:
                        path += ' ≫ '+col.collection.theme2
                        if col.collection.theme3:
                            path += ' ≫ '+col.collection.theme3
                d = {
                    'id': col.collection.ref,
                    'name': col.collection.name,
                    'creator': functions.format_user(col.collection.user, 'dam', 'html'),
                    'path': path
                }
                collections.append(d)
            context['collections'] = collections
            tables.append(['collections', 'fa-th-large', 'Collections'])
        if tables != []:
            context['tables'] = tables
            context['table_options'] = {
                'responsive': 'true',
                'dom': '''"<'sub-card-header d-flex'<'card-header-title'>fr><'card-body't>"''',
                'stateSave': 'true',
                'select': {'style': 'single'},
                'scrollY': 150,
                'deferRender': 'true',
                'scroller': 'true',
                'language': {
                    'searchPlaceholder': 'Search',
                    'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
                    },
                }
        context['image_url'] = functions.get_dam_preview(self.object.ref)
        return context

    def get_object(self):
        """ Raise a 404 instead of exception on things that aren't proper UUIDs"""
        try:
            object = super().get_object()
            return object
        except ObjectDoesNotExist:
            raise Http404


@method_decorator(login_required, name='dispatch')
class PageList(DTListView):
    breadcrumb = [('Pages', '/pages')]
    list_name = 'pages'
    dt_field_list = ['name', 'dam_id', 'order']


@method_decorator(login_required, name='dispatch')
class PageDetail(DetailView):
    model = Page
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = ['Pages']
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context = functions.set_menus(self.request, context, state)
        page_title = self.object.name
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        # context['form'] = forms.page_main(instance=self.object)
        return context


@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'dalme_app/index.html'
    default_cards = ['cards/counter_articles.html',
                     'cards/counter_assets.html',
                     'cards/counter_inventories.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Dashboard', '')]
        if self.request.session.get('sidebar_toggle') is not None:
            sidebar_toggle = self.request.session['sidebar_toggle']
        else:
            sidebar_toggle = ''
            self.request.session['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['sidebar_toggle'] = sidebar_toggle
        context = functions.set_menus(self.request, context, state)
        page_title = 'Dashboard'
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        return context


def PageManifest(request, pk):
    context = {}
    page = Page.objects.get(pk=pk)
    context['page'] = page
    context['canvas'] = page.get_canvas()
    return render(request, 'dalme_app/page_manifest.html', context)


@method_decorator(login_required, name='dispatch')
class SetList(DTListView):
    breadcrumb = [('Project', ''), ('Sets', '/sets')]
    list_name = 'sets'
    dt_editor_options = {'idSrc': '"id"'}
    dte_field_list = ['name', 'set_type', 'is_public', 'has_landing', 'description', 'owner', 'set_permissions']
    dt_options = {
        'pageLength': 25,
        'paging': 'true',
        'responsive': 'true',
        'fixedHeader': 'true',
        'dom': '\'<"card-table-header"B<"btn-group ml-auto"f>r><"#filters-container.collapse.clearfix"><"panel-container"<"panel-left"t>><"sub-card-footer"ip>\'',
        'serverSide': 'true',
        'stateSave': 'true',
        'select': {'style': 'single'},
        'deferRender': 'true',
        'rowId': '"id"',
        'processing': 'true',
        'language': {
            'searchPlaceholder': 'Search',
            'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
            },
        'order': '[[ 1, "asc" ]]'
        }

    def get_dte_buttons(self, *args, **kwargs):
        dte_buttons = []
        if self.request.user.has_perm('dalme_app.change_set'):
            dte_buttons.append({'extend': 'edit', 'text': '<i class="fa fa-pen fa-sm dt_menu_icon"></i> Edit Selected', 'formTitle': 'Edit Set Information'})
        if self.request.user.has_perm('dalme_app.delete_set'):
            dte_buttons.append({'extend': 'remove', 'text': '<i class="fa fa-times fa-fw dt_menu_icon"></i> Delete Selected', 'formTitle': 'Delete Set',
                                'formMessage': 'Are you sure you wish to remove this set from the database? This action cannot be undone.'})
        return dte_buttons


@method_decorator(login_required, name='dispatch')
class SetsDetail(DetailView):
    model = RightsPolicy
    template_name = 'dalme_app/set_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Project', ''), ('Sets', '/sets')]
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context = functions.set_menus(self.request, context, state)
        page_title = self.object.name
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        context['object_class'] = 'Set'
        context['object_icon'] = 'fas fa-folder'
        if self.object.is_public:
            public = '<i class="fas fa-check-square"></i>'
        else:
            public = '<i class="far fa-square"></i>'
        if self.object.has_landing:
            landing = '<i class="fas fa-check-square"></i>'
        else:
            landing = '<i class="far fa-square"></i>'
        context['object_attributes'] = {
            'ID': self.object.id,
            'Name': self.object.name,
            'Type': self.object.get_set_type_display(),
            'Public': public,
            'Landing': landing,
            'Endpoint': '<span class="text-capitalize">{}</span>'.format(self.object.endpoint),
            'Owner': '<a href="/user/{}">{} ({})</a>'.format(self.object.owner.id, self.object.owner.profile.full_name, self.object.owner.username),
            'Permissions': self.object.get_set_permissions_display(),
            'Description': self.object.description,
            'Progress': str(self.object.workset_progress) + '%',
        }
        members = self.object.members.all()
        context['members'] = members
        tables = ['members', 'fa-plus-square', 'Set Members ({})'.format(members.count())]
        if tables != []:
            context['tables'] = tables
            context['table_options'] = {
                'responsive': 'true',
                'dom': '''"<'sub-card-header d-flex'<'card-header-title'>Bfr><'card-body't>"''',
                'stateSave': 'true',
                'select': {'style': 'multi'},
                'scrollY': '''"calc(100vh - 600px)"''',
                'deferRender': 'true',
                'scroller': 'true',
                'rowId': '"id"',
                'language': {
                    'searchPlaceholder': 'Search',
                    'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
                },
                'buttons': "[{text: '<i class=\"fa fa-trash-alt fa-fw\"></i>', action: function (e, dt, node, config) {delete_set_members(dt)}, className: \"align-self-end\"}]"
            }
        return context

    def get_object(self):
        """ Raise a 404 instead of exception on things that aren't proper UUIDs"""
        try:
            object = Set.objects.get(pk=self.kwargs['pk'])
            return object
        except ObjectDoesNotExist:
            raise Http404


@method_decorator(login_required, name='dispatch')
class SetsRedirect(View):
    def get(self, request, *args, **kwargs):
        workset = get_object_or_404(Set, pk=kwargs['pk'])
        members = Source.objects.filter(sets__set_id=workset.id)
        try:
            current = members.filter(sets__workset_done=False)[0]
        except IndexError:
            current = members[-1]
        url = '/{}/{}/?set={}'.format(workset.endpoint, current.id, workset.id)
        return HttpResponseRedirect(url)


@method_decorator(login_required, name='dispatch')
class Scripts(TemplateView):
    template_name = 'dalme_app/scripts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Scripts', '')]
        sidebar_toggle = self.request.session['sidebar_toggle']
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['sidebar_toggle'] = sidebar_toggle
        context = functions.set_menus(self.request, context, state)
        context['scripts'] = custom_scripts.get_script_menu()
        page_title = 'Custom Scripts'
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        if self.request.GET.get('s') is not None:
            context['output'] = eval('custom_scripts.'+self.request.GET['s']+'(self.request)')
        return context


@method_decorator(login_required, name='dispatch')
class TicketDetail(DetailView):
    model = Ticket
    template_name = 'dalme_app/ticket_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Project', ''), ('Issue Tickets', '/tickets')]
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context = functions.set_menus(self.request, context, state)
        page_title = 'Ticket #'+str(self.object.id)
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        context['ticket'] = self.object
        return context

    def get_object(self):
        try:
            object = super().get_object()
            return object
        except ObjectDoesNotExist:
            raise Http404


@method_decorator(login_required, name='dispatch')
class TicketList(DTListView):
    breadcrumb = [('Project', ''), ('Issue Tickets', '/tickets')]
    list_name = 'tickets'
    dt_options = {
        'pageLength': 25,
        'paging': 'true',
        'responsive': 'true',
        'fixedHeader': 'true',
        'dom': '\'<"card-table-header"B<"btn-group ml-auto"f>r><"#filters-container.collapse.clearfix"><"panel-container"<"panel-left"t>><"sub-card-footer"ip>\'',
        'serverSide': 'true',
        'stateSave': 'true',
        'select': {'style': 'single'},
        'deferRender': 'true',
        'rowId': '"id"',
        'processing': 'true',
        'language': {
            'searchPlaceholder': 'Search',
            'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
            },
        'order': '[[ 0, "desc" ]]'
        }


@method_decorator(login_required, name='dispatch')
class TasksDetail(DetailView):
    model = Task
    template_name = 'dalme_app/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Project', ''), ('Tasks', '/tasks')]
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context = functions.set_menus(self.request, context, state)
        page_title = 'Task #'+str(self.object.id)+' ('+self.object.task_list.name+')'
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        context['task'] = self.object
        return context

    def get_object(self):
        try:
            object = super().get_object()
            return object
        except ObjectDoesNotExist:
            raise Http404


@method_decorator(login_required, name='dispatch')
class TasksList(TemplateView):
    template_name = 'dalme_app/tasks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Project', ''), ('Tasks', '/tasks')]
        sidebar_toggle = self.request.session['sidebar_toggle']
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['sidebar_toggle'] = sidebar_toggle
        context = functions.set_menus(self.request, context, state)
        page_title = 'Task Manager'
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        # Superusers see all lists
        if self.request.user.is_superuser:
            lists = TaskList.objects.all().order_by('group', 'name')
        else:
            lists = TaskList.objects.filter(group__in=self.request.user.groups.all()).order_by('group', 'name')
        list_count = lists.count()
        # superusers see all lists, so count shouldn't filter by just lists the admin belongs to
        if self.request.user.is_superuser:
            task_count = Task.objects.filter(completed=0).count()
        else:
            task_count = Task.objects.filter(completed=0).filter(task_list__group__in=self.request.user.groups.all()).count()
        context['lists'] = lists
        context['list_count'] = list_count
        context['task_count'] = task_count
        context['tables'] = [
            ['lists', 'fa-tasks', 'Lists', {
                'ajax': '"/api/tasklists/?format=json"',
                'serverSide': 'true',
                'responsive': 'true',
                'dom': '''"<'sub-card-header d-flex'<'card-header-title'><'dt-btn-group'>r><'card-body't><'sub-card-footer'i>"''',
                'select': {'style': 'single'},
                'scrollResize': 'true',
                'scrollY': '"82vh"',
                'scrollX': '"100%"',
                'deferRender': 'true',
                'scroller': 'true',
                'rowId': '"id"',
                'order': '[ 1, "asc" ]',
                'rowGroup': '{dataSrc: \'group\'}',
                'columnDefs': [
                      {
                          'title': '"List"',
                          'targets': 0,
                          'data': '"name"'
                      },
                      {
                          'title': '"Group"',
                          'targets': 1,
                          'data': '"group"',
                          "visible": 'false'
                      }
                      ]
                }
             ],
            ['tasks', 'fa-calendar-check', 'Tasks', {
                'ajax': '"/api/tasks/?format=json"',
                'serverSide': 'true',
                'responsive': 'true',
                'dom': '''"<'sub-card-header d-flex'<'card-header-title'><'dt-btn-group'>fr><'card-body't><'sub-card-footer'i>"''',
                'select': {'style': 'single'},
                'scrollResize': 'true',
                'scrollY': '"82vh"',
                'scrollX': '"100%"',
                'deferRender': 'true',
                'scroller': 'true',
                'language': {
                    'searchPlaceholder': 'Search',
                    'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
                    },
                'rowId': '"id"',
                'columnDefs': [
                      {
                          'title': '"Task"',
                          'targets': 0,
                          'data': '"task"',
                          'visible': 1,
                          "orderData": '[ 6, 7 ]',
                          'searchable': 0
                      },
                      {
                          'title': '"Dates"',
                          'targets': 1,
                          'data': '"dates"',
                          'visible': 1,
                          "orderData": '[ 5, 7 ]',
                          'searchable': 0
                      },
                      {
                          'title': '"Assigned to"',
                          'targets': 2,
                          'data': '"assigned_to"',
                          'visible': 1,
                          'searchable': 0
                      },
                      {
                          'title': '"Attachments"',
                          'targets': 3,
                          'data': '"attachments"',
                          'visible': 1,
                          'orderable': 0,
                          'searchable': 0,
                      },
                      {
                          'title': '"Done"',
                          'targets': 4,
                          'data': '"completed"',
                          'render': 'function ( data, type, row, meta ) {return data == true ? \'<i class="fa fa-check-circle dt_checkbox_true"></i>\' : \'<i class="fa fa-times-circle dt_checkbox_false"></i>\';}',
                          'className': '"td-center"',
                          'width': '"19px"',
                          'visible': 1,
                          'searchable': 0
                      },
                      {
                          'title': '"Due date"',
                          'targets': 5,
                          'data': '"due_date"',
                          'visible': 0,
                      },
                      {
                          'title': '"Title"',
                          'targets': 6,
                          'data': '"title"',
                          'visible': 0,
                      },
                      {
                          'title': '"Created"',
                          'targets': 7,
                          'data': '"creation_timestamp"',
                          'visible': 0,
                      },
                      {
                          'title': '"Description"',
                          'targets': 8,
                          'data': '"description"',
                          'visible': 0,
                      }
                  ]
                }
             ]
        ]
        return context
