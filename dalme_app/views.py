from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connections
from django.db.models import Q, Count, F, Prefetch
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.template.defaulttags import register
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.base import TemplateView
from django_celery_results.models import TaskResult
from django.db.models.query import QuerySet
import requests, uuid, os, datetime, json
from allaccess.views import OAuthCallback
from rest_framework import viewsets, status
from dalme_app.serializers import SourceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from dalme_app import functions, custom_scripts
from dalme_app.menus import menu_constructor
from dalme_app.models import *
from dalme_app.tasks import parse_inventory
from django.db.models.functions import Concat
from django.db.models import CharField, Value
from django.db.models.expressions import RawSQL
from haystack.generic_views import SearchView
from django.http import HttpResponse
import urllib.parse as urlparse
import logging
logger = logging.getLogger(__name__)


class OAuthCallback_WP(OAuthCallback):
    logger.debug("OAuthCallback_WP called")
    def get_or_create_user(self, provider, access, info):
        uname = info['user_login']
        email = info['email']
        name = info['display_name']
        #User = get_user_model()
        try:
            logger.debug("OAuthCallback_WP tries to get user")
            the_user = User.objects.get(username=uname)
        except Entry.DoesNotExist:
            logger.debug("OAuthCallback_WP fails to get user, tries to create it")
            the_user = User.objects.create_user(uname, email, None)
            the_user.profile.full_name = name
            the_user.save()
        return the_user

def SessionUpdate(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])
    if request.POST['var'] == 'sidebar_toggle':
        if request.session['sidebar_toggle'] == '':
            request.session['sidebar_toggle'] = 'toggled'
        else:
            request.session['sidebar_toggle'] = ''
    return HttpResponse('ok')

@method_decorator(login_required,name='dispatch')
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

@method_decorator(login_required,name='dispatch')
class DTListView(TemplateView):
    """ Generic list view that feeds Datatables """
    template_name = 'dalme_app/dtlistview.html'
    breadcrumb = []
    dt_options = {
        'pageLength':25,
        'paging': 'true',
        'responsive':'true',
        'fixedHeader': 'true',
        'dom': '\'<"card-table-header"B<"btn-group ml-auto"f>r><"#filters-container.collapse.clearfix"><"panel-container"<"panel-left"t>><"sub-card-footer"ip>\'',
        'serverSide': 'true',
        'stateSave': 'true',
        'select': { 'style': 'single'},
        'deferRender': 'true',
        'rowId': '"id"',
        'language': {'searchPlaceholder': 'Search'}
        }
    dt_buttons = [{ 'extend': '"colvis"', 'text': '"\uf0db"'}]
    dt_buttons_extra = ['"pageLength"']
    dt_editor_buttons = [
        { 'extend': 'create', 'text': '\uf067 Add' },
        { 'extend': 'edit', 'text': '\uf304 Edit' },
        { 'extend': 'remove', 'text': '\uf00d Delete' },
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
        context['preview'] = self.get_preview()
        return context

    def get_list_name(self, *args, **kwargs):
        try:
            list_name = self.list_name
        except:
            list_name = None
        return list_name

    def get_list(self, list_name, *args, **kwargs):
        try:
            _list = DT_list.objects.get(short_name=list_name)
        except:
            _list = None
        return _list

    def get_fields_dict(self, _list, *args, **kwargs):
        try:
            fields = [
                'field__short_name',
                'field__name',
                'orderable',
                'visible',
                'searchable',
                'render_exp',
                'dte_type',
                'dte_options',
                'dte_message',
                'dt_class_name',
                'dte_class_name',
                'dt_width',
                'dt_name',
                'dte_name',
                'nowrap',
                'dte_opts',
                'is_filter',
                'filter_options',
                'filter_mode',
                'filter_type',
                'filter_operator',
                'filter_lookup'
            ]
            qset = DT_fields.objects.filter(list=_list.id).values(*fields)
            fields_dict = {}
            for i in qset:
                fields_dict[i['field__short_name']] = i
        except:
            fields_dict = None
        return fields_dict

    def get_breadcrumb(self, *args, **kwargs):
        try:
            breadcrumb = self.breadcrumb
        except:
            breadcrumb = None
        return breadcrumb

    def get_page_title(self, _list, *args, **kwargs):
        try:
            title = _list.name
        except:
            title = None
        return title

    def get_dt_options(self, _list, fields_dict, *args, **kwargs):
        dt_options = {}
        options = self.dt_options
        options['ajax'] = self.get_dt_ajax_str(_list)
        dt_options['options'] = options
        dt_options['buttons'] = self.dt_buttons
        dt_options['buttons_extra'] = self.dt_buttons_extra
        dt_options['columnDefs'] = self.get_dt_column_defs(_list, fields_dict)
        return dt_options

    def get_dt_ajax_str(self, _list, *args, **kwargs):
        try:
            base_url = _list.api_url
            dt_ajax_str = '"'+base_url+'?format=json"'
        except:
            dt_ajax_str = None
        return dt_ajax_str

    def get_dt_column_defs(self, _list, fields_dict, *args, **kwargs):
        dt_fields = self.get_dt_fields(_list)
        column_defs = []
        col = 0
        for f in dt_fields:
            lf = fields_dict[f]
            c_dict = {}
            dt_name = lf['field__short_name']
            if lf['dt_name']:
                dt_name = lf['dt_name']
            c_dict['title'] = '"'+lf['field__name']+'"'
            c_dict['targets'] = col
            c_dict['data'] = '"'+dt_name+'"'
            c_dict['defaultContent'] = '""'
            if not lf['visible']:
                c_dict['visible'] = 'false'
            if not lf['orderable']:
                c_dict['orderable'] = 'false'
            if not lf['searchable']:
                c_dict['searchable'] = 'false'
            if lf['render_exp']:
                c_dict['render'] = lf['render_exp']
            if lf['dt_width']:
                c_dict['width'] = '"'+lf['dt_width']+'"'
            if lf['dt_class_name'] and lf['nowrap']:
                c_dict['className'] = '"' + lf['dt_class_name'] + ' nowrap"'
            elif lf['dt_class_name']:
                c_dict['className'] = '"' + lf['dt_class_name'] + '"'
            elif lf['nowrap']:
                c_dict['className'] = '"nowrap"'
            column_defs.append(c_dict)
            col = col + 1
        return column_defs

    def get_dt_fields(self, _list, *args, **kwargs):
        try:
            dt_fields = self.dt_field_list
        except:
            dt_fields = None
        return dt_fields

    def get_dte_fields(self, _list, *args, **kwargs):
        if self.dte_field_list:
            dte_fields = self.dte_field_list
        else:
            dte_fields = None
        return dte_fields

    def get_dt_editor(self, _list, fields_dict, *args, **kwargs):
        if self.get_dte_fields(_list):
            dte_fields = self.get_dte_fields(_list)
            dt_editor = {}
            dt_editor['ajax_url'] = _list.api_url
            fields = []
            for f in dte_fields:
                lf = fields_dict[f]
                f_dict = {}
                f_name = lf['field__short_name']
                if lf['dt_name']:
                    f_name = lf['dt_name']
                if lf['dte_name']:
                    f_name = lf['dte_name']
                f_dict['label'] = lf['field__name']
                f_dict['name'] = f_name
                if lf['dte_type']:
                    if lf['dte_type'] == 'multi-chosen':
                        f_dict['type'] = 'chosen'
                        f_dict['attr'] = { 'multiple': 'true' }
                    else:
                        f_dict['type'] = lf['dte_type']
                if lf['dte_opts']:
                    if lf['dte_type'] == 'autocomplete':
                        ac_opts = eval(lf['dte_opts'])
                    else:
                        f_dict['opts'] = eval(lf['dte_opts'])
                if lf['dte_options']:
                    if lf['dte_type'] == 'autoComplete':
                        try:
                            ac_opts['source'] = functions.get_dte_options(lf['dte_options'], lf['dte_type'])
                        except:
                            ac_opts = { 'source': functions.get_dte_options(lf['dte_options'], lf['dte_type'])}
                        f_dict['opts'] = ac_opts
                    else:
                        f_dict['options'] = functions.get_dte_options(lf['dte_options'], lf['dte_type'])
                if lf['dte_message']:
                    f_dict['message'] = lf['dte_message']
                fields.append(f_dict)
            dt_editor['fields'] = fields
            if self.get_dte_options():
                dt_editor['options'] = self.get_dte_options()
            if self.get_dte_buttons():
                dt_editor['buttons'] = self.get_dte_buttons()
        else:
            dt_editor = None
        return dt_editor

    def get_filters(self, fields_dict, *args, **kwargs):
        try:
            filters = []
            for key, dict in fields_dict.items():
                if dict['is_filter']:
                    filter = {}
                    filter['label'] = dict['field__name']
                    filter['field'] = key
                    filter['type'] = dict['filter_type']
                    filter['operator'] = dict['filter_operator']
                    if 'lookup' in filter:
                        filter['lookup'] = dict['filter_lookup']
                    if dict['filter_type'] == 'text':
                        filter['lookups'] = [
                                {'label':'is', 'lookup':'exact'},
                                {'label':'contains', 'lookup':'contains'},
                                {'label':'in', 'lookup':'in'},
                                {'label':'starts with', 'lookup':'startswith'},
                                {'label':'ends with', 'lookup':'endswith'},
                                {'label':'matches regex', 'lookup':'regex'},
                        ]
                    elif dict['filter_type'] == 'check' or dict['filter_type'] == 'select':
                        values = eval(dict['filter_options'])
                        filter = functions.add_filter_options(values, filter, dict['filter_mode'])
                    filters.append(filter)
            if filters == []:
                filters = None
        except:
            filters = None
        return filters

    def get_helpers(self, _list, *args, **kwargs):
        try:
            helpers = _list.helpers.split(',')
        except:
            helpers = None
        return helpers

    def get_preview(self, *args, **kwargs):
        try:
            preview = self.preview
        except:
            preview = False
        return preview

    def get_dte_options(self, *args, **kwargs):
        try:
            dte_options = self.dt_editor_options
        except:
            dte_options = False
        return dte_options

    def get_dte_buttons(self, *args, **kwargs):
        try:
            dte_buttons = self.dt_editor_buttons
        except:
            dte_buttons = False
        return dte_buttons

@method_decorator(login_required,name='dispatch')
class ModelLists(DTListView):
    template_name = 'dalme_app/models.html'
    dt_editor_options = {'idSrc': '"id"'}
    dt_options = {
        'serverSide': 'true',
        'responsive': 'true',
        'dom': '\'<"sub-card-header-embed d-flex"B<"#fieldsets.btn-group mr-auto"><"btn-group"f>r><"card-body"t><"sub-card-footer"i>\'',
        'stateSave': 'true',
        'select': { 'style': 'single'},
        'scrollResize': 'true',
        'scrollY': '"50vh"',
        'deferRender': 'true',
        'scroller': 'true',
        'language': {'searchPlaceholder': 'Search'},
        'rowId': '"id"',
    }
    dt_buttons = [{ 'extend': '"colvis"', 'text': '"\uf0db"'}]
    dt_buttons_extra = None

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
            qs = Content_class.objects.all()
            parent_class_opt = {i.id:i.name for i in qs}
            context['parent_class'] = {
                'name': 'content class',
                'options': parent_class_opt
            }
        elif model == 'attribute_types':
            qs = Content_type.objects.all()
            parent_class_opt = {i.id:i.name for i in qs}
            context['parent_class'] = {
                'name': 'content type',
                'options': parent_class_opt
            }
        elif model == 'dt_fields':
            context['dt_fieldsets'] = {'DT Fields': [3,4,5,6,7,8,9,10], 'DTE Fields': [11,12,13,14,15,16], 'Filter Fields': [17,18,19,20,21,22]}
            qs = DT_list.objects.all()
            parent_class_opt = {i.id:i.name for i in qs}
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
        return context

    def get_list_name(self, *args, **kwargs):
        return self.kwargs['model']

    def get_breadcrumb(self, *args, **kwargs):
        if self.kwargs['model'] == 'dt_fields':
            breadcrumb = [('Data Models', ''), ( 'DataTables Fields', '/models/dt_fields')]
        else:
            breadcrumb = [('Data Models', ''),(self.kwargs['model'].replace('_',' ').title(), '/models/'+self.kwargs['model'])]
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
            dt_field_list = ['id', 'name', 'short_name', 'description', 'data_type', 'source', 'same_as']
        elif model == 'dt_fields':
            dt_field_list = ['id', 'list','field','dt_name','orderable','visible','searchable','nowrap','render_exp','dt_class_name','dt_width','dte_name','dte_type','dte_options','dte_opts','dte_message','dte_class_name','is_filter','filter_type','filter_mode','filter_operator','filter_options','filter_lookup']
        return dt_field_list

    def get_dte_fields(self, _list, *args, **kwargs):
        model = self.kwargs['model']
        if model == 'content_types':
            dte_fields = ['name', 'short_name', 'content_class', 'description', 'attribute_types']
        elif model == 'attribute_types':
            dte_fields = ['name', 'short_name', 'description', 'data_type', 'source', 'same_as']
        elif model == 'dt_fields':
            dte_fields = ['dt_name','orderable','visible','searchable','nowrap','render_exp','dt_class_name','dt_width','dte_name','dte_type','dte_options','dte_opts','dte_message','dte_class_name','is_filter','filter_type','filter_mode','filter_operator','filter_options','filter_lookup']
        else:
            dte_fields = None
        return dte_fields

    def get_dte_buttons(self, *args, **kwargs):
        model = self.kwargs['model']
        dte_buttons = [ { 'extend': 'create', 'text': '\uf067 Add' } ]
        if model != 'dt_fields':
            dte_buttons.append({ 'extend': 'edit', 'text': '\uf304 Edit' })
        dte_buttons.append({ 'extend': 'remove', 'text': '\uf00d Delete' })
        return dte_buttons

@method_decorator(login_required,name='dispatch')
class SourceList(DTListView):
    """ Lists sources """
    def get_list_name(self, *args, **kwargs):
        list_name = 'all'
        if 'type' in self.request.GET:
            list_name = self.request.GET['type']
        return list_name

    def get_breadcrumb(self, *args, **kwargs):
        type = self.get_list_name()
        if type == 'all':
            breadcrumb = [('Sources', ''),('All Sources', '/sources')]
        elif type == 'inventories':
            breadcrumb = [('Repository',''), ('Inventories','/sources?type=inventories')]
        else:
            list_label = DT_list.objects.get(short_name=type).name
            breadcrumb = [('Sources', ''), (list_label, '/sources?type='+type)]
        return breadcrumb

    def get_dt_ajax_str(self, _list, *args, **kwargs):
        base_url = _list.api_url
        type = _list.short_name
        if type == 'sources':
            dt_ajax_str = '"'+base_url+'?format=json"'
        else:
            dt_ajax_str = '"'+base_url+'?format=json&type='+type+'"'
        return dt_ajax_str

    def get_dt_fields(self, _list, *args, **kwargs):
        dt_fields = DT_fields.objects.filter(list=_list).values_list('field__short_name', flat=True)
        return dt_fields

@method_decorator(login_required,name='dispatch')
class SourceDetail(DetailView):
    model = Source
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        if self.object.parent_source:
            source_data['Parent'] = '<a href="{}">{}</a>'.format('/sources/'+str(self.object.parent_source.id),self.object.parent_source.name)
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
            order = Content_attributes.objects.get(content_type_id=self.object.type,attribute_type_id=a.attribute_type).order
            value = functions.get_attribute_value(a)
            dict = {
                'label': label,
                'value': value,
                'order': order
            }
            attribute_data.append(dict)
        attribute_data = sorted(attribute_data, key=lambda x:x['order'])
        context['attribute_data'] = attribute_data
        tables = []
        if is_inv and has_pages:
            folios = functions.get_editor_folios(self.object)
            context['folio_count'] = folios['folio_count']
            context['folio_menu'] = folios['folio_menu']
            context['folio_list'] = folios['folio_list']
            tables.append(['pages','fa-book-open','Pages'])
        if has_children:
            context['children'] = self.object.source_set.all().order_by('name')
            tables.append(['children','fa-sitemap','Children'])
        if tables != []:
            context['tables'] = tables
            context['table_options'] = {
                'responsive':'true',
                'dom': '''"<'sub-card-header d-flex'<'card-header-title'>fr><'card-body't>"''',
                'stateSave': 'true',
                'select': { 'style': 'single'},
                'scrollY': 150,
                'deferRender': 'true',
                'scroller': 'true',
                'language': '{searchPlaceholder: "Search"}'
                }
        return context

    def get_breadcrumb(self, *args, **kwargs):
        try:
            request = self.request
            ref = request.META.get('HTTP_REFERER', '/')
            parsed_ref = urlparse.urlparse(ref)
            s_type = urlparse.parse_qs(parsed_ref.query)['type'][0]
        except:
            s_type = 'all'
        if s_type == 'all':
            breadcrumb = [('Sources', ''),('All Sources', '/sources')]
        elif s_type == 'inventories':
            breadcrumb = [('Repository',''), ('Inventories','/sources?type=inventories')]
        else:
            list_label = DT_list.objects.get(short_name=s_type).name
            breadcrumb = [('Sources', ''), (list_label, '/sources?type='+s_type)]
        return breadcrumb

    def get_object(self):
        """ Raise a 404 instead of exception on things that aren't proper UUIDs """
        try:
            object = super().get_object()
            return object
        except:
            raise Http404

def SourceManifest(request, pk):
    context = {}
    source = Source.objects.get(pk=pk)
    context['source'] = source
    context['page_canvases'] = [page.get_canvas() for page in source.pages.all()]
    return render(request, 'dalme_app/source_manifest.html', context)

@method_decorator(login_required,name='dispatch')
class UserList(DTListView):
    """ Lists users and allows editing and creation of new records via the API """
    list_name = 'users'
    breadcrumb = [('Project', ''),('Users', '/users')]
    dt_editor_options = {'idSrc': '"id"'}
    dt_field_list = ['id','last_login', 'is_superuser', 'username', 'full_name', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'groups', 'date_joined', 'dam_usergroup', 'wiki_groups', 'wp_role']
    dte_field_list = ['first_name', 'last_name', 'full_name', 'email', 'username', 'password', 'is_staff', 'is_superuser', 'groups', 'dam_usergroup', 'wiki_groups', 'wp_role']

@method_decorator(login_required,name='dispatch')
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
            #'Wiki groups': self.object.wiki_user__wiki_groups,
            #'DAM group': self.object.dam_user.usergroup,
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
        except:
            raise Http404

@method_decorator(login_required,name='dispatch')
class ImageList(DTListView):
    breadcrumb = [('Repository', ''),('Images', '/images')]
    list_name = 'images'
    dt_field_list = ['ref','field8', 'field79', 'has_image', 'field12', 'creation_date', 'created_by', 'field3', 'collections', 'field51']
    preview = True

@method_decorator(login_required,name='dispatch')
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
                res_type_obj = rs_resource_type_field.objects.get(ref=a.resource_type_field)
                name = res_type_obj.name
                label = res_type_obj.title
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
            for c in col_list:
                col = rs_collection.objects.get(ref=c.collection)
                path = ''
                if col.theme:
                    path += col.theme
                    if col.theme2:
                        path += ' ≫ '+col.theme2
                        if col.theme3:
                            path += ' ≫ '+col.theme3
                dict = {
                    'id': col.ref,
                    'name': col.name,
                    'creator': functions.format_user(col.user, 'dam','html'),
                    'path': path
                }
                collections.append(dict)
            context['collections'] = collections
            tables.append(['collections','fa-th-large','Collections'])
        if tables != []:
            context['tables'] = tables
            context['table_options'] = {
                'responsive':'true',
                'dom': '''"<'sub-card-header d-flex'<'card-header-title'>fr><'card-body't>"''',
                'stateSave': 'true',
                'select': { 'style': 'single'},
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
        except:
            raise Http404

@method_decorator(login_required,name='dispatch')
class PageList(DTListView):
    breadcrumb = [('Repository', ''),('Pages', '/pages')]
    list_name = 'pages'
    dt_field_list = ['name', 'dam_id', 'order']

@method_decorator(login_required,name='dispatch')
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
        context['form'] = forms.page_main(instance=self.object)
        return context

@method_decorator(login_required,name='dispatch')
class Index(TemplateView):
    template_name = 'dalme_app/index.html'
    default_cards = [
    'cards/counter_articles.html',
    'cards/counter_assets.html',
    'cards/counter_inventories.html'
    ]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Dashboard', '')]
        try:
            sidebar_toggle = self.request.session['sidebar_toggle']
        except:
            self.request.session['sidebar_toggle'] = ''
            sidebar_toggle = self.request.session['sidebar_toggle']
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['sidebar_toggle'] = sidebar_toggle
        context = functions.set_menus(self.request, context, state)
        page_title = 'Dashboard'
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        tables = []
        if Workset.objects.filter(owner=self.request.user).exists():
            context['worksets'] = Workset.objects.filter(owner=self.request.user)
            tables.append(['worksets','fa-layer-group', 'My Worksets'])
        if Task.objects.filter(assigned_to=self.request.user.id, completed=0).exists():
            context['tasks'] = Task.objects.filter(assigned_to=self.request.user.id, completed=0)
            tables.append(['tasks','fa-tasks', 'My Tasks'])
        if tables != []:
            context['tables'] = tables
            context['table_options'] = {
                'responsive':'true',
                'dom': '''"<'sub-card-header d-flex'<'card-header-title'><'dt-btn-group'>fr><'card-body't>"''',
                'stateSave': 'true',
                'select': { 'style': 'single'},
                'scrollY': 200,
                'deferRender': 'true',
                'scroller': 'true',
                'language': '{searchPlaceholder: "Search"}'
                }
        context['cards'] = self.default_cards
        context['counters'] = functions.get_counters(['wiki_articles', 'dam_assets', 'inventories'])
        return context

def PageManifest(request, pk):
    context = {}
    page = Page.objects.get(pk=pk)
    context['page'] = page
    context['canvas'] = page.get_canvas()
    return render(request, 'dalme_app/page_manifest.html', context)

@method_decorator(login_required,name='dispatch')
class UIRefMain(View):
    """ Routes requests to UIRef views """
    def get(self, request, *args, **kwargs):
        if 'm' in self.request.GET:
            template = 'UI_reference/'+self.request.GET['m']+'.html'
            breadcrumb = [('UI Reference', ''), (self.request.GET['m'].capitalize(), template)]
            view = UIRef.as_view(template_name=template)
        return view(request, breadcrumb=breadcrumb)

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

@method_decorator(login_required,name='dispatch')
class Scripts(TemplateView):
    template_name = 'dalme_app/scripts.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        breadcrumb = [('Scripts', '')]
        sidebar_toggle = self.request.session['sidebar_toggle']
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['sidebar_toggle'] = sidebar_toggle
        context = functions.set_menus(self.request, context, state)
        context['scripts'] = custom_scripts.get_script_menu()
        page_title = 'Custom Scripts'
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        if 's' in self.request.GET:
            scpt = self.request.GET['s']
            context['output'] = eval('custom_scripts.'+scpt+'(request)')
        return context

@method_decorator(login_required,name='dispatch')
class TasksList(TemplateView):
    template_name = 'dalme_app/tasks.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        breadcrumb = [('Project', ''),('Tasks', '/tasks')]
        sidebar_toggle = self.request.session['sidebar_toggle']
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['sidebar_toggle'] = sidebar_toggle
        context = functions.set_menus(self.request, context, state)
        page_title = 'Task Manager'
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        # Superusers see all lists
        if request.user.is_superuser:
            lists = TaskList.objects.all().order_by('group', 'name')
        else:
            lists = TaskList.objects.filter(group__in=request.user.groups.all()).order_by('group', 'name')
        list_count = lists.count()
        # superusers see all lists, so count shouldn't filter by just lists the admin belongs to
        if request.user.is_superuser:
            task_count = Task.objects.filter(completed=0).count()
        else:
            task_count = Task.objects.filter(completed=0).filter(task_list__group__in=request.user.groups.all()).count()

        context['lists'] = lists
        context['list_count'] = list_count
        context['task_count'] = task_count
        context['tables'] = [
            ['lists','fa-tasks', 'Lists', {
                'ajax': '"../api/tasklists/?format=json"',
                'serverSide': 'true',
                'responsive':'true',
                'dom': '''"<'sub-card-header d-flex'<'card-header-title'><'dt-btn-group'>r><'card-body't><'sub-card-footer'i>"''',
                'stateSave': 'true',
                'select': { 'style': 'single'},
                'scrollY': '"75vh"',
                'deferRender': 'true',
                'scroller': 'true',
                'rowGroup': {
                    'dataSrc': "group"
                },
                'rowId': '"id"',
                'columnDefs':[
                      {
                          'title':'"List"',
                          'targets':0,
                          'data':'"name"'
                      },
                      {
                          'title':'"Group"',
                          'targets':1,
                          'data':'"group"',
                          "visible":'false'
                      }
                  ]
                }
            ],
            ['tasks','fa-check-square', 'Tasks', {
                'ajax': '"../api/tasks/?format=json"',
                'serverSide': 'true',
                'responsive':'true',
                'dom': '''"<'sub-card-header d-flex'<'card-header-title'><'dt-btn-group'>fr><'card-body't><'sub-card-footer'i>"''',
                'stateSave': 'true',
                'select': { 'style': 'single'},
                'scrollY': '"75vh"',
                'deferRender': 'true',
                'scroller': 'true',
                'language': '{searchPlaceholder: "Search"}',
                'rowId': '"id"',
                'columnDefs':[
                      {
                          'title':'"Task"',
                          'targets':0,
                          'data':'"title"'
                      },
                      {
                          'title':'"Description"',
                          'targets':1,
                          'data':'"description"'
                      },
                      {
                          'title':'"Due date"',
                          'targets':2,
                          'data':'"due_date"'
                      },
                      {
                          'title':'"Assigned to"',
                          'targets':3,
                          'data':'"assigned_to"'
                      },
                      {
                          'title':'"Created by"',
                          'targets':4,
                          'data':'"created_by"'
                      },
                      {
                          'title':'"Created on"',
                          'targets':5,
                          'data':'"creation_timestamp"'
                      }
                  ]
                }
            ]
        ]
        return context
