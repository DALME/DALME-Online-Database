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
from allaccess.views import OAuthCallback
from dalme_app import functions, custom_scripts
from dalme_app.models import (Profile, Content_class, Content_type, DT_list, DT_fields, Page,
                              Source, Workset, TaskList, Task, rs_resource, rs_collection_resource,
                              rs_resource_data, rs_resource_type_field, rs_user, wiki_user_groups, Language,
                              Attribute_type, Country, rs_collection, Ticket)
from haystack.generic_views import SearchView
import urllib.parse as urlparse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.conf import settings


class OAuthCallback_WP(OAuthCallback):
    def get_or_create_user(self, provider, access, info):
        uname = info['user_login']
        email = info['email']
        name = info['display_name']
        # User = get_user_model()
        try:
            the_user = User.objects.get(username=uname)
        except User.DoesNotExist:
            the_user = User.objects.create_user(uname, email, None)
            the_user.profile.full_name = name
            the_user.save()
        return the_user


def SessionUpdate(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])
    if request.POST['var'] == 'sidebar_toggle':
        if request.session['sidebar_toggle'] == '':
            request.session['sidebar_toggle'] = 'toggled'
        else:
            request.session['sidebar_toggle'] = ''
    return HttpResponse('ok')


def DownloadAttachment(request, path):
    path_tokens = path.split('/')
    original_filename = path_tokens.pop(-1)
    file_path = settings.MEDIA_ROOT + '/' + path
    fp = open(file_path, 'rb')
    response = HttpResponse(fp.read())
    fp.close()
    type, encoding = mimetypes.guess_type(original_filename)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = str(os.stat(file_path).st_size)
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
        'language': {'searchPlaceholder': 'Search'}
        }
    dt_buttons = [
        {'extend': 'colvis', 'text': '<i class="fa fa-columns fa-fw"></i>'},
        {'extend': "pageLength"}
    ]
    dt_editor_buttons = [
        {'extend': 'create', 'text': '<i class="fa fa-plus fa-fw dt_menu_icon"></i> Create New'},
        {'extend': 'edit', 'text': '<i class="fa fa-pen fa-sm dt_menu_icon"></i> Edit Selected'},
        {'extend': 'remove', 'text': '<i class="fa fa-times fa-fw dt_menu_icon"></i> Delete Selected'},
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
        try:
            _list = DT_list.objects.get(short_name=list_name)
        except DT_list.DoesNotExist:
            _list = None
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
                        f_dict['message'] = lf['dte_message']
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
        for key, dict in fields_dict.items():
            if dict['is_filter']:
                filter = {}
                filter['label'] = dict['field__name']
                filter['field'] = key
                if dict.get('filter_type') is not None:
                    filter['type'] = dict['filter_type']
                else:
                    filter['type'] = 'text'
                if dict.get('filter_lookup') is not None:
                    filter['lookup'] = dict['filter_lookup']
                if filter['type'] in types_w_lookups:
                    filter['lookups'] = functions.get_filter_lookups(filter['type'])
                if filter['type'] == 'check' or filter['type'] == 'select':
                    if dict.get('filter_mode') is not None:
                        f_mode = dict['filter_mode']
                    else:
                        f_mode = 'complete'
                    if dict.get('filter_options') is not None:
                        # values = eval(dict['filter_options'])
                        values = dict['filter_options']
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
        'language': {'searchPlaceholder': 'Search'},
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
            dt_field_list = ['id', 'name', 'short_name', 'content_class', 'description', 'attribute_types']
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
            dte_fields = ['name', 'short_name', 'content_class', 'description', 'attribute_types']
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
    dte_field_list = ['name', 'short_name', 'type', 'parent', 'is_inventory']
    dt_editor_buttons = [
        {'extend': 'create', 'text': '<i class="fa fa-plus fa-fw dt_menu_icon"></i> Create New', 'formTitle': 'Create New Source'},
        {'extend': 'edit', 'text': '<i class="fa fa-pen fa-sm dt_menu_icon"></i> Edit Selected', 'formTitle': 'Edit Source Information'},
        {'extend': 'remove', 'text': '<i class="fa fa-times fa-fw dt_menu_icon"></i> Delete Selected', 'formTitle': 'Delete Source',
         'formMessage': 'Are you sure you wish to remove this source from the database? This action cannot be undone.'},
    ]

    def get_list_name(self, *args, **kwargs):
        list_name = 'all'
        if 'type' in self.request.GET:
            list_name = self.request.GET['type']
        return list_name

    def get_breadcrumb(self, *args, **kwargs):
        _type = self.get_list_name()
        if _type == 'all':
            breadcrumb = [('Sources', ''), ('All Sources', '/sources')]
        elif _type == 'inventories':
            breadcrumb = [('Repository', ''), ('Inventories', '/sources?type=inventories')]
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
            if self.request.GET['type'] == 'inventories':
                module_list = ['filters']
        return module_list


@method_decorator(login_required, name='dispatch')
class SourceDetail(DetailView):
    model = Source

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'workset' in self.request.GET:
            workset = Workset.objects.get(pk=self.request.GET['workset'])
            qset = json.loads(workset.qset)
            seq = workset.current_record
            para = {
                'workset_id': workset.id,
                'name': workset.name,
                'description': workset.description,
                'current': seq,
                'prev_id': qset.get(str(int(seq)-1), {}).get('pk', "none"),
                'next_id': qset.get(str(int(seq)+1), {}).get('pk', "none"),
                'total': len(qset),
                'endpoint': workset.endpoint,
                'progress': round(workset.progress, 2)
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
        is_inv = self.object.is_inventory
        has_pages = len(self.object.pages.all()) > 0
        has_children = len(self.object.source_set.all()) > 0
        context['is_inv'] = is_inv
        context['has_pages'] = has_pages
        context['has_children'] = has_children
        source_data = {
            'Type': self.object.type.name,
            'Name': self.object.name,
            'Short name': self.object.short_name,
            'Inventory?': functions.format_boolean(is_inv),
        }
        if self.object.parent:
            source_data['Parent'] = '<a href="{}">{}</a>'.format('/sources/'+str(self.object.parent.id), self.object.parent.name)
        context['source_data'] = source_data
        context['source_metadata'] = {
            'ID': str(self.object.id),
            'Created': functions.format_rct(self.object.creation_username, self.object.creation_timestamp),
            'Modified': functions.format_rct(self.object.modification_username, self.object.modification_timestamp),
        }
        attribute_data = []
        attributes = self.object.attributes.all().select_related('attribute_type')
        for a in attributes:
            label = a.attribute_type.name
            value = functions.get_attribute_value(a)
            dict = {
                'label': label,
                'value': value,
            }
            attribute_data.append(dict)
        context['attribute_data'] = attribute_data
        tables = []
        if is_inv and has_pages:
            folios = functions.get_editor_folios(self.object)
            context['folio_count'] = folios['folio_count']
            context['folio_menu'] = folios['folio_menu']
            context['folio_list'] = folios['folio_list']
            tables.append(['pages', 'fa-book-open', 'Pages'])
        if has_children:
            context['children'] = self.object.source_set.all().order_by('name')
            tables.append(['children', 'fa-sitemap', 'Children'])
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
                'language': '{searchPlaceholder: "Search"}'
                }
        return context

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
    dt_editor_buttons = [
        {'extend': 'create', 'text': '<i class="fa fa-plus fa-fw dt_menu_icon"></i> Create New', 'formTitle': 'Create New User'},
        {'extend': 'edit', 'text': '<i class="fa fa-pen fa-sm dt_menu_icon"></i> Edit Selected', 'formTitle': 'Edit User Information'},
        {'extend': 'remove', 'text': '<i class="fa fa-times fa-fw dt_menu_icon"></i> Delete Selected', 'formTitle': 'Delete User'},
    ]


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
        'language': {'searchPlaceholder': 'Search'},
        'order': '[[ 0, "desc" ]]'
        }


@method_decorator(login_required, name='dispatch')
class CountryList(DTListView):
    breadcrumb = [('System', ''), ('Countries', '/countries')]
    list_name = 'countries'
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
        'language': {'searchPlaceholder': 'Search'},
        'order': '[[ 1, "asc" ]]'
        }


@method_decorator(login_required, name='dispatch')
class CityList(DTListView):
    breadcrumb = [('System', ''), ('Cities', '/cities')]
    list_name = 'cities'
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
        'language': {'searchPlaceholder': 'Search'},
        'order': '[[ 1, "asc" ]]'
        }


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
        'language': {'searchPlaceholder': 'Search'}
        }


@method_decorator(login_required, name='dispatch')
class ImageList(DTListView):
    breadcrumb = [('Repository', ''), ('Images', '/images')]
    list_name = 'images'
    # dt_field_list = ['ref', 'field8', 'field79', 'has_image', 'field12', 'creation_date', 'created_by', 'field3', 'collections', 'field51']
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
        # 'select': { 'style': 'multi', 'selector': 'td:first-child'},
        'select': {'style': 'multi'},
        'deferRender': 'true',
        'rowId': '"id"',
        'language': {'searchPlaceholder': 'Search'},
        # 'order': '[[ 1, "asc" ]]'
        }
    dt_editor_buttons = [
        {'extend': 'edit', 'text': '<i class="fa fa-pen fa-sm dt_menu_icon"></i> Edit Selected', 'formTitle': 'Edit Image Information'},
        {'action': 'toggle_inline_edit()', 'text': '<i class="fa fa-edit fa-fw dt_menu_icon"></i> Edit Inline', 'className': "inline-edit-toggle"},
        {'extend': 'remove', 'text': '<i class="fa fa-times fa-fw dt_menu_icon"></i> Delete Selected', 'formTitle': 'Delete Image',
         'formMessage': 'Are you sure you wish to remove this image from the DAM? This action cannot be undone.'},
        {'extend': 'selectNone', 'text': '<i class="fa fa-broom fa-fw dt_menu_icon"></i> Clear Selection'},
        {'extend': 'selected', 'action': 'create_source_from_selected()', 'text': '<i class="fa fa-plus-square fa-fw dt_menu_icon"></i> Create Source from Selection'}
    ]
    module_list = ['preview', 'filters']


@method_decorator(login_required, name='dispatch')
class ImageDetail(DetailView):
    model = rs_resource
    template_name = 'dalme_app/image_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Repository', ''), ('Images', '/images')]
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
                dict = {
                    'name': name,
                    'label': label,
                    'value': value,
                }
                attribute_data.append(dict)
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
                dict = {
                    'id': col.collection.ref,
                    'name': col.collection.name,
                    'creator': functions.format_user(col.collection.user, 'dam', 'html'),
                    'path': path
                }
                collections.append(dict)
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
                'language': '{searchPlaceholder: "Search"}'
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
    breadcrumb = [('Repository', ''), ('Pages', '/pages')]
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
class UIRefMain(View):
    """ Routes requests to UIRef views """
    def get(self, request, *args, **kwargs):
        if self.request.GET.get('m') is not None:
            template = 'UI_reference/'+self.request.GET['m']+'.html'
            breadcrumb = [('UI Reference', ''), (self.request.GET['m'].capitalize(), template)]
            view = UIRef.as_view(template_name=template)
        return view(request, breadcrumb=breadcrumb)


@method_decorator(login_required, name='dispatch')
class WorksetsRedirect(View):
    def get(self, request, *args, **kwargs):
        workset = get_object_or_404(Workset, pk=kwargs['pk'])
        qset = json.loads(workset.qset)
        seq = str(workset.current_record + 1)
        seq_id = qset[seq]['pk']
        # para = {
        #     'workset': workset.id,
        #     'name': workset.name,
        #     'description': workset.description,
        #     'current': seq,
        #     'prev_id': qset.get(str(int(seq)-1), {}).get('pk', "none"),
        #     'next_id': qset.get(str(int(seq)+1), {}).get('pk', "none"),
        #     'total': len(qset),
        #     'endpoint': workset.endpoint,
        #     'progress': round(workset.progress, 2)
        # }
        url = '/{}/{}/?workset={}'.format(workset.endpoint, seq_id, workset.id)
        # url += '&'.join(['{}={}'.format(key, value) for key, value in para.items()])
        # return redirect('/website/')
        return HttpResponseRedirect(url)


class UIRef(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = self.kwargs['breadcrumb']
        sidebar_toggle = self.request.session['sidebar_toggle']
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['sidebar_toggle'] = sidebar_toggle
        context = functions.set_menus(self.request, context, state)
        context['page_chain'] = functions.get_page_chain(breadcrumb)
        return context


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
        context['comments'] = True
        return context

    def get_object(self):
        try:
            object = super().get_object()
            return object
        except ObjectDoesNotExist:
            raise Http404


@method_decorator(login_required, name='dispatch')
class TicketList(DTListView):
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
        'language': {'searchPlaceholder': 'Search'},
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
        context['comments'] = True
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
                'language': '{searchPlaceholder: "Search"}',
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
