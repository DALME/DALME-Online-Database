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
    #form_class = dalme_searchform

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
        'responsive':'true',
        'fixedHeader': 'true',
        'dom': '\'<"card-table-header"B<"#filters-button-ct.dt-buttons">fr><"#filters-container.collapse.clearfix"><"card-table-body"tip>\'',
        'serverSide': 'true',
        'stateSave': 'true',
        'select': 'true',
        'deferRender': 'true',
        'language': {'searchPlaceholder': 'Search'}
        }
    dt_buttons = [{ 'extend': '"colvis"', 'text': '"\uf0db"'}]
    dt_buttons_extra = ['"pageLength"']
    dt_editor_options = None
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
        list = DT_list.objects.get(short_name=list_name)
        fields_dict = self.get_fields_dict(list)
        page_title = self.get_page_title(list)
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        context['dt_options'] = self.get_dt_options(list, fields_dict)
        context['dt_editor'] = self.get_dt_editor(list, fields_dict)
        context['filters'] = self.get_filters(fields_dict)
        context['form_helper'] = self.get_form_helper(list)
        return context

    def get_list_name(self, *args, **kwargs):
        return self.list_name

    def get_fields_dict(self, list, *args, **kwargs):
        fields = [
            'field__short_name',
            'field__name',
            'orderable',
            'visible',
            'searchable',
            'render_exp',
            'dte_type',
            'dte_options',
            'dt_name',
            'dte_name',
            'nowrap',
            'dte_opts',
            'is_filter',
            'filter_options',
            'filter_mode',
            'filter_type',
            'filter_operator'
        ]
        qset = DT_fields.objects.filter(list=list.id).values(*fields)
        fields_dict = {}
        for i in qset:
            fields_dict[i['field__short_name']] = i
        return fields_dict

    def get_breadcrumb(self, *args, **kwargs):
        return self.breadcrumb

    def get_page_title(self, list, *args, **kwargs):
        title = list.name
        return title

    def get_dt_options(self, list, fields_dict, *args, **kwargs):
        dt_options = {}
        options = self.dt_options
        options['ajax'] = self.get_dt_ajax_str(list)
        dt_options['options'] = options
        dt_options['buttons'] = self.dt_buttons
        dt_options['buttons_extra'] = self.dt_buttons_extra
        dt_options['columnDefs'] = self.get_dt_column_defs(list, fields_dict)
        return dt_options

    def get_dt_ajax_str(self, list, *args, **kwargs):
        base_url = list.api_url
        dt_ajax_str = '"'+base_url+'?format=json"'
        return dt_ajax_str

    def get_dt_column_defs(self, list, fields_dict, *args, **kwargs):
        dt_fields = self.get_dt_fields(list)
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
            if lf['nowrap']:
                c_dict['className'] = '"nowrap"'
            column_defs.append(c_dict)
            col = col + 1
        return column_defs

    def get_dt_fields(self, list, *args, **kwargs):
        return self.dt_field_list

    def get_dte_fields(self, list, *args, **kwargs):
        if self.dte_field_list:
            dte_fields = self.dte_field_list
        else:
            dte_fields = None
        return dte_fields

    def get_dt_editor(self, list, fields_dict, *args, **kwargs):
        if self.get_dte_fields(list):
            dte_fields = self.get_dte_fields(list)
            dt_editor = {}
            dt_editor['ajax_url'] = list.api_url
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
                    f_dict['type'] = lf['dte_type']
                if lf['dte_opts']:
                    f_dict['opts'] = eval(lf['dte_opts'])
                if lf['dte_options']:
                    f_dict['options'] = self.get_dte_options(lf['dte_options'], lf['dte_type'])
                fields.append(f_dict)
            dt_editor['fields'] = fields
            if self.dt_editor_options:
                dt_editor['options'] = self.dt_editor_options
            if self.dt_editor_buttons:
                dt_editor['buttons'] = self.dt_editor_buttons
        else:
            dt_editor = None
        return dt_editor

    def get_dte_options(self, options, field_type, *args, **kwargs):
        if field_type == 'chosen':
            opts = [{'label': "", 'value': ""}]
        else:
            opts = []
        options = eval(options)
        if type(options) is dict:
            opts.append(options)
        elif type(options) is list:
            q = eval(options[0])
            if isinstance(q, QuerySet):
                for e in q:
                    opt = { 'label': getattr(e, options[1]), 'value': getattr(e, options[2]) }
                    opts.append(opt)
            elif isinstance(q, tuple):
                for value, label in q:
                    opt = { 'label': label, 'value': value }
                    opts.append(opt)
        return opts

    def get_filters(self, fields_dict, *args, **kwargs):
        filters = []
        for key, dict in fields_dict.items():
            if dict['is_filter']:
                filter = {}
                filter['label'] = dict['field__name']
                filter['field'] = key
                filter['type'] = dict['filter_type']
                filter['operator'] = dict['filter_operator']
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
        return filters

    def get_form_helper(self, list, *args, **kwargs):
        if list.form_helper:
            form_helper = list.form_helper
        else:
            form_helper = None
        return form_helper

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

    def get_dt_ajax_str(self, list, *args, **kwargs):
        base_url = list.api_url
        type = list.short_name
        if type == 'sources':
            dt_ajax_str = '"'+base_url+'?format=json"'
        else:
            dt_ajax_str = '"'+base_url+'?format=json&type='+type+'"'
        return dt_ajax_str

    def get_dt_fields(self, list, *args, **kwargs):
        dt_fields = DT_fields.objects.filter(list=list).values_list('field__short_name', flat=True)
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
        }
        if is_inv:
            source_data['Inventory?'] = '<i class="fa fa-check-circle dt_checkbox_true"></i>'
        else:
            source_data['Inventory?'] = '<i class="fa fa-times-circle dt_checkbox_false"></i>'
        if self.object.parent_source:
            name = self.object.parent_source.name
            url = '/sources/'+str(self.object.parent_source.id)
            source_data['Parent'] = '<a href="{}">{}</a>'.format(url,name)
        context['source_data'] = source_data
        created = self.object.creation_timestamp.strftime('%d-%b-%Y@%H:%M')
        modified = self.object.modification_timestamp.strftime('%d-%b-%Y@%H:%M')
        c_user = Profile.objects.get(user__username=self.object.creation_username)
        created_user = '<a href="/user/{}">{}</a>'.format(c_user.user_id, c_user.full_name)
        m_user = Profile.objects.get(user__username=self.object.modification_username)
        modified_user = '<a href="/user/{}">{}</a>'.format(m_user.user_id, m_user.full_name)
        context['source_metadata'] = {
            'ID': str(self.object.id),
            'Created': created+' by '+created_user,
            'Modified': modified+' by '+modified_user
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
        if is_inv and has_pages:
            folios = functions.get_editor_folios(self.object)
            context['folio_count'] = folios['folio_count']
            context['folio_menu'] = folios['folio_menu']
            context['folio_list'] = folios['folio_list']
            context['table_options_pages'] = {
                'pageLength':5,
                'responsive':'true',
                'dom': '''"<'sub-card-header clearfix'<'card-header-title'>r><'card-body'tip>"''',
                'stateSave': 'true',
                'select': 'true',
                'paging': 'true',
                'language': '{searchPlaceholder: "Search..."}',
                'order': [[ 3, "asc" ]]
                }
        if has_children:
            context['children'] = self.object.source_set.all().order_by('name')
            context['table_options_children'] = {
                'pageLength':5,
                'responsive':'true',
                'dom': '''"<'sub-card-header clearfix'<'card-header-title'>r><'card-body'tip>"''',
                'stateSave': 'true',
                'select': 'true',
                'paging': 'true',
                'language': '{searchPlaceholder: "Search..."}'
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
        if type == 'all':
            breadcrumb = [('Sources', ''),('All Sources', '/sources')]
        elif type == 'inventories':
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
class AdminMain(View):
    """ Routes requests to admin views """
    def get(self, request, *args, **kwargs):
        if 'type' in self.request.GET:
            type = self.request.GET['type']
            title = 'List of '+type.capitalize()
            view = eval('Admin'+type.capitalize()).as_view()
        return view(request, title=title)

class AdminUsers(DTListView):
    """ Lists users and allows editing and creation of new records via the API """
    list_name = 'users'
    breadcrumb = [('System', ''),('Users', '/admin?type=users')]
    dt_editor_options = {'idSrc': '"id"'}
    dt_field_list = ['id','last_login', 'is_superuser', 'username', 'full_name', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'groups', 'date_joined', 'dam_usergroup', 'wiki_groups', 'wp_role']
    dte_field_list = ['first_name', 'last_name', 'full_name', 'email', 'username', 'password', 'is_staff', 'is_superuser', 'groups', 'dam_usergroup', 'wiki_groups', 'wp_role']

class AdminNotifications(DTListView):
    breadcrumb = [('System', ''),('Notifications', '/admin?type=notifications')]
    dt_ajax_base_url = '../api/notifications/'
    dt_column_headers = [
            ['Id', 'id', 0],
            ['Code', 'code', 1],
            ['Level','level', 1],
            ['Text','text', 1],
            ['Type','type', 1]
            ]
    dt_render_dict = {
            'Level': 'function ( data, type, row, meta ) {return \'<div class="dt_n_level dt_n_level_\'+data.display+\'">\'+data.display+\'</div>\';}',
            'Type': 'function ( data, type, row, meta ) {return \'<div class="dt_n_type">\'+data.display+\'</div>\';}'
            }
    dt_editor_options = {'idSrc': '"id"',}
    dt_editor_fields = [
            {'label':"Code:", 'name': "code"},
            {'label':"Level:", 'name': "level.value", 'type': "chosen",
                'opts': {
                    "disable_search": 'true',
                },
                'options': [
                  {'label': "Debug", 'value': "10"},
                  {'label': "Info", 'value': "20"},
                  {'label': "Success", 'value': "25"},
                  {'label': "Warning", 'value': "30"},
                  {'label': "Error", 'value': "40"}
                ]},
             {'label':"Text:", 'name': "text"},
             {'label':"Type:", 'name': "type.value", 'type': "radio",
                'options': [
                  {'label': "Modal", 'value': "1"},
                  {'label': "Notification", 'value': "2"}
                ],}
        ]

class AdminModels(TemplateView):
    template_name = 'dalme_app/dtlistview_models.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('System', ''), ('Data Models', '/admin?type=models')]
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        column_headers_content = [
                ['ID', 'id', 1],
                ['Class','content_class', 0],
                ['Name','name', 1],
                ['Short name','short_name', 0],
                ['Description','description', 1]]
        column_headers_attributes = [
                ['ID', 'id', 1],
                ['Name','name', 1],
                ['Short name','short_name', 1],
                ['Description','description', 0],
                ['DType','data_type', 1],
                ['Order','order', 1]]
        render_dict_content = {
                'Username': '''function ( data, type, row, meta ) {return '<a href="/user/'+data+'">'+data+'</a>';}''',
                'Email': '''function ( data, type, row, meta ) {return '<a href="'+data.url+'">'+data.name+'</a>';}''',
                'Last login': '''function ( data ) {return moment(data).format("DD-MMM-YYYY@HH:mm");}''',
                'Date joined': '''function ( data ) {return moment(data).format("DD-MMM-YYYY@HH:mm");}''',
                'SU': '''function ( data, type, row, meta ) {return data == true ? '<i class="fa fa-check-circle dt_checkbox_true"></i>' : '<i class="fa fa-times-circle dt_checkbox_false"></i>';}''',
                'Staff': '''function ( data, type, row, meta ) {return data == true ? '<i class="fa fa-check-circle dt_checkbox_true"></i>' : '<i class="fa fa-times-circle dt_checkbox_false"></i>';}''',
                'Active': '''function ( data, type, row, meta ) {return data == true ? '<i class="fa fa-check-circle dt_checkbox_true"></i>' : '<i class="fa fa-times-circle dt_checkbox_false"></i>';}''',
                }
        render_dict_attributes = {}
        context = functions.set_menus(self.request, context, state)
        context['columnDefs_content'] = self.get_column_defs(column_headers_content, render_dict_content)
        context['columnDefs_attributes'] = self.get_column_defs(column_headers_attributes, render_dict_attributes)
        context['table_options_content'] = {
            'pageLength':25,
            'responsive':'true',
            'dom': '''"<'#content_card.card-header'<'#c-title'><'#c-classes_button'>B><'card-body't>"''',
            'serverSide': 'true',
            'stateSave': 'true',
            'select': '{style: "single"}',
            'ajax': '"../api/models/?type=content&format=json"',
            'scrollY': '100',
            'scrollResize': 'true',
            'deferRender': 'true',
            'scroller': 'true',
            'rowId': '"id"',
            }
        context['table_options_attributes'] = {
            'pageLength':25,
            'responsive':'true',
            'dom': '''"<'#attribute_card.card-header'<'#a-title'>B><'card-body't>"''',
            'serverSide': 'true',
            'stateSave': 'true',
            'select': '{style: "single"}',
            'ajax': '"../api/models/?type=attributes&format=json"',
            'scrollY': '100',
            'scrollResize': 'true',
            'deferRender': 'true',
            'scroller': 'true',
            'rowId': '"id"',
            }

        classes = Content_class.objects.all()
        classes_button = '<button class="btn btn-secondary btn-sm dropdown-toggle" type="button" id="classes_menu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Class: All</button><div class="dropdown-menu dropdown-menu-right" aria-labelledby="classes_menu"><a class="dropdown-item" href="#">Add new...</a><div class="dropdown-divider"></div><a class="dropdown-item" href="#" onclick="class_select(0, \\\'All\\\')">All</a>'
        for c in classes:
            classes_button += '<a class="dropdown-item" href="#" onclick="class_select({},\\\'{}\\\')">{}</a>'.format(c.id, c.name, c.name)
        classes_button += '</div>'

        context['classes_button'] = classes_button
        context['table_buttons_content'] = ['{ extend: "colvis", text: "\uf0db" }']
        context['table_buttons_attributes'] = ['{ extend: "colvis", text: "\uf0db", className: "btn_single"}']
        context['page_title'] = 'System Data Models'

        return context

    def get_column_defs(self, column_headers, render_dict):
        columnDefs = []
        col = 0
        for i in column_headers:
            c_dict = {}
            c_dict['title'] = '"'+i[0]+'"'
            c_dict['targets'] = col
            c_dict['data'] = '"'+i[1]+'"'
            c_dict['defaultContent'] = '"-"'
            if i[2]:
                c_dict['visible'] = 'true'
            else:
                c_dict['visible'] = 'false'
            if i[0] in render_dict:
                c_dict['render'] = render_dict[i[0]]
            columnDefs.append(c_dict)
            col = col + 1
        return columnDefs

@method_decorator(login_required,name='dispatch')
class ImageList(DTListView):
    breadcrumb = [('Repository', ''),('Images', '/images')]
    list_name = 'images'
    dt_field_list = ['ref','field8', 'field79', 'has_image', 'field12', 'creation_date', 'created_by', 'field3', 'collections', 'field51']

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
            'Creator': functions.get_dam_user(self.object.created_by, 'html'),
            'Record modified': functions.format_date(self.object.modified, 'timestamp'),
            'File modified': functions.format_date(self.object.file_modified, 'timestamp'),
            'Filesize': self.object.file_size,
        }
        if self.object.has_image:
            image_data['Image?'] = '<i class="fa fa-check-circle dt_checkbox_true"></i>'
        else:
            image_data['Image?'] = '<i class="fa fa-times-circle dt_checkbox_false"></i>'
        context['image_data'] = image_data
        try:
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
        except:
            attribute_data = None
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
                'creator': functions.get_dam_user(col.user, 'html'),
                'path': path
            }
            collections.append(dict)
        context['collections'] = collections
        context['table_options'] = {
            'pageLength':5,
            'responsive':'true',
            'dom': '''"<'sub-card-header clearfix'<'card-header-title'>r><'card-body'tip>"''',
            'stateSave': 'true',
            'select': 'true',
            'paging': 'true',
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
        context['tiles'] = menu_constructor(self.request, 'tile_item', 'home_tiles_default.json', state)
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
        breadcrumb = [('Dev Scripts', '')]
        sidebar_toggle = self.request.session['sidebar_toggle']
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['sidebar_toggle'] = sidebar_toggle
        context = functions.set_menus(self.request, context, state)
        context['scripts'] = custom_scripts.get_script_menu()
        page_title = 'Dev Scripts'
        context['page_title'] = page_title
        context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
        if 's' in self.request.GET:
            scpt = self.request.GET['s']
            context['output'] = eval('custom_scripts.'+scpt+'(request)')
        return context
