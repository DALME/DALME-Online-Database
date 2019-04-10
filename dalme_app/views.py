from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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

import requests, uuid, os, datetime, json
from allaccess.views import OAuthCallback

from rest_framework import viewsets, status
from dalme_app.serializers import SourceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from dalme_app import functions, custom_scripts, forms
from dalme_app.menus import menu_constructor
from dalme_app.models import *

from dalme_app.tasks import parse_inventory
from django.db.models.functions import Concat
from django.db.models import CharField, Value
from django.db.models.expressions import RawSQL

from haystack.generic_views import SearchView
from django.http import HttpResponse

import logging
logger = logging.getLogger(__name__)


#authentication (sub)classses
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = ['Search']
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context = functions.set_menus(self.request, context, state)
        context['page_title'] = 'Search Results'

        return context

class DTListView(TemplateView):
    template_name = 'dalme_app/dtlistview.html'
    breadcrumb = []
    table_options = {
        'pageLength':25,
        'responsive':'true',
        'dom': '''"<'card-table-header'Bfr><'card-table-body'tip>"''',
        'serverSide': 'true',
        'stateSave': 'true',
        'select': 'true',
        'deferRender': 'true',
        'language': '{searchPlaceholder: "Search..."}'
        }
    table_buttons = ['{ extend: "colvis", text: "\uf0db", className: "btn_single"}']
    column_headers = []
    render_dict = {}
    nowrap_list = []
    ajax_string = ''
    table_editor = None
    filters = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = self.get_breadcrumb()
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context = functions.set_menus(self.request, context, state)
        context['page_title'] = self.get_page_title()
        context['columnDefs'] = self.get_column_defs()
        context['table_options'] = self.get_table_options()
        context['table_buttons'] = self.get_table_buttons()
        context['table_editor'] = self.get_table_editor()
        context['filters'] = self.get_filters()

        return context

    def get_table_options(self, *args, **kwargs):
        table_options = self.table_options
        table_options['ajax'] = self.get_table_ajax_str()
        return table_options

    def get_page_title(self, *args, **kwargs):
        try:
            p_title = self.kwargs['title']
        except:
            try:
                p_title = self.page_title
            except:
                p_title = 'List View'
        return p_title

    def get_table_buttons(self, *args, **kwargs):
        return self.table_buttons

    def get_filters(self, *args, **kwargs):
        return self.filters

    def get_breadcrumb(self, *args, **kwargs):
        return self.breadcrumb

    def get_table_editor(self, *args, **kwargs):
        return self.table_editor

    def get_column_headers(self, *args, **kwargs):
        return self.column_headers

    def get_column_defs(self, *args, **kwargs):
        #create column headers
        column_headers = self.get_column_headers()
        render_dict = self.render_dict
        nowrap_list = self.nowrap_list
        #create column definitions for DT
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
            if i[0] in nowrap_list:
                c_dict['className'] = '"nowrap"'
            columnDefs.append(c_dict)
            col = col + 1
        return columnDefs

    def get_table_ajax_str(self, *args, **kwargs):
        return self.ajax_string

@method_decorator(login_required,name='dispatch')
class SourceMain(View):
    """
    Collects views to be displayed from the root of sources. GET requests to
    this endpoint will list sources, while POST requests will handle creating
    new sources.
    """

    def get(self, request, *args, **kwargs):
        """Display list of sources"""
        view = SourceList.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handle creating new sources"""
        view = SourceCreate.as_view()
        return view(request, *args, **kwargs)

@method_decorator(login_required,name='dispatch')
class AdminMain(View):
    """
    Routes requests to admin views
    """
    def get(self, request, *args, **kwargs):
        if 'type' in self.request.GET:
            type = self.request.GET['type']
            title = 'List of '+type.capitalize()
            view = eval('Admin'+type.capitalize()).as_view()
        return view(request, title=title)

class AdminUsers(DTListView):
    breadcrumb = ['System','Users']
    ajax_string = '"../api/users/?format=json"'
    column_headers = [
            ['ID', 'id', 1],
            ['Last login','last_login', 1],
            ['SU','is_superuser', 1],
            ['Username','username', 1],
            ['Full name','full_name', 1],
            ['First name','first_name', 0],
            ['Last name','last_name', 0],
            ['Email','email', 1],
            ['Staff','is_staff', 0],
            ['Active','is_active', 1],
            ['Date joined','date_joined', 0],
            ['DAM user group','dam_usergroup', 0],
            ['DAM user ID','dam_userid', 0],
            ['Wiki groups','wiki_groups', 0],
            ['Wiki user ID','wiki_userid', 0],
            ['Wiki username','wiki_username', 0],
            ['WordPress user ID','wp_userid', 0],
            ['WordPress role','wp_role', 0]]
    render_dict = {
            'Username': '''function ( data, type, row, meta ) {return '<a href="/user/'+data+'">'+data+'</a>';}''',
            'Email': '''function ( data, type, row, meta ) {return '<a href="'+data.url+'">'+data.name+'</a>';}''',
            'Last login': '''function ( data ) {return moment(data).format("DD-MMM-YYYY@HH:mm");}''',
            'Date joined': '''function ( data ) {return moment(data).format("DD-MMM-YYYY@HH:mm");}''',
            'SU': '''function ( data, type, row, meta ) {return data == true ? '<i class="fa fa-check-circle dt_checkbox_true"></i>' : '<i class="fa fa-times-circle dt_checkbox_false"></i>';}''',
            'Staff': '''function ( data, type, row, meta ) {return data == true ? '<i class="fa fa-check-circle dt_checkbox_true"></i>' : '<i class="fa fa-times-circle dt_checkbox_false"></i>';}''',
            'Active': '''function ( data, type, row, meta ) {return data == true ? '<i class="fa fa-check-circle dt_checkbox_true"></i>' : '<i class="fa fa-times-circle dt_checkbox_false"></i>';}''',
            }
    nowrap_list = []

class AdminNotifications(DTListView):
    breadcrumb = ['System','Notifications']
    table_options = {
        'pageLength':25,
        'responsive':'true',
        'dom': '''"<'card-table-header'Bfr><'card-table-body'tip>"''',
        'serverSide': 'true',
        'stateSave': 'true',
        'deferRender': 'true',
        'language': '{searchPlaceholder: "Search..."}'
        }
    ajax_string = '"../api/notifications/?format=json"'
    table_buttons = [
        '{ extend: "colvis", text: "\uf0db" }',
        '{ extend: "create", text: "\uf067", editor: editor }',
        '{ extend: "edit", text: "\uf304", editor: editor }',
        '{ extend: "remove", text: "\uf00d", editor: editor }'
        ]
    column_headers = [
            ['Id', 'id', 0],
            ['Code', 'code', 1],
            ['Level','level', 1],
            ['Text','text', 1],
            ['Type','type', 1]
            ]
    render_dict = {
            'Level': '''function ( data, type, row, meta ) {return '<div class="dt_n_level dt_n_level_'+data.display+'">'+data.display+'</div>';}''',
            'Type': '''function ( data, type, row, meta ) {return '<div class="dt_n_type">'+data.display+'</div>';}'''
            }
    nowrap_list = []
    table_editor = {
            'ajax_url': '../api/notifications/',
            'idSrc': '"id"',
            'fields': [
                {'label':"Code:", 'name': "code"},
                {'label':"Level:", 'name': "level.value", 'type': "select",
                    'options': [
                      {'label': "DEBUG", 'value': "10"},
                      {'label': "INFO", 'value': "20"},
                      {'label': "SUCCESS", 'value': "25"},
                      {'label': "WARNING", 'value': "30"},
                      {'label': "ERROR", 'value': "40"}
                    ]},
                 {'label':"Text:", 'name': "text"},
                 {'label':"Type:", 'name': "type.value", 'type': "radio",
                    'options': [
                      {'label': "MODAL", 'value': "1"},
                      {'label': "NOTIFICATION", 'value': "2"}
                    ],}
            ]
            }

class AdminModels(TemplateView):
    template_name = 'dalme_app/dtlistview_models.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = ['System', 'Data Models']
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


class SourceList(DTListView):
    table_options = {
        'pageLength':25,
        'responsive':'true',
        'fixedHeader': 'true',
        'dom': '''"<'card-table-header'Bfr><'card-table-body'tip>"''',
        'serverSide': 'true',
        'stateSave': 'true',
        'deferRender': 'true',
        'paging': 'true',
        'language': '{searchPlaceholder: "Search..."}'
        }
    table_buttons = [
        '{ extend: "colvis", text: "\uf0db" }',
        '"pageLength"'
        ]
    render_dict = {
        'Name': '''function ( data, type, row, meta ) {return (typeof data == 'undefined') ? "" : '<a href="'+data.url+'">'+data.name+'</a>';}''',
        'Web address': '''function ( data, type, row, meta ) {return (typeof data == 'undefined') ? "" : '<a href="'+data.url+'">'+data.name+'</a>';}''',
        'Parent': '''function ( data, type, row, meta ) {return (typeof data == 'undefined') ? "" : '<a href="'+data.url+'">'+data.name+'</a>';}''',
        'Inv': '''function ( data, type, row, meta ) {return data == true ? '<i class="fa fa-check-circle dt_checkbox_true"></i>' : '<i class="fa fa-times-circle dt_checkbox_false"></i>';}'''
        }
    nowrap_list = ['Type']

    def get_type(self):
        if 'type' in self.request.GET:
            return self.request.GET['type']
        else:
            return ''

    def get_list_type(self, type):
        return Content_list.objects.get(short_name=type)

    def get_table_ajax_str(self, *args, **kwargs):
        type = self.get_type()
        if type == '':
            ajax_string = '"../api/sources/?format=json"'
        else:
            ajax_string = '"../api/sources/?format=json&type=' + type + '"'
        return ajax_string

    def get_breadcrumb(self, *args, **kwargs):
        type = self.get_type()
        if type == '':
            breadcrumb = ['Sources', 'All']
        elif type == 'inventories':
            breadcrumb = ['Repository', 'Inventories']
        else:
            breadcrumb = ['Sources', self.get_list_type(type).name]
        return breadcrumb

    def get_page_title(self, *args, **kwargs):
        type = self.get_type()
        if type == '':
            page_title = "Sources"
        else:
            page_title = 'List of '+ self.get_list_type(type).name
        return page_title

    def get_column_headers(self, *args, **kwargs):
        type = self.get_type()
        if type == '':
            def_headers = ['15']
            extra_headers = ['type']
            ct_l = Content_type.objects.filter(content_class=1)
            att_l = Attribute_type.objects.filter(content_type__in=ct_l)
        else:
            list_type = self.get_list_type(type)
            def_headers = list_type.default_headers.split(',')
            if list_type.extra_headers:
                extra_headers = list_type.extra_headers.split(',')
            else:
                extra_headers = []
            q_obj = Q()
            if type == 'inventories':
                att_l = Content_type.objects.get(pk=13).attribute_types.all()
                extra_headers.append('no_folios')
            else:
                content_types = list_type.content_types.all()
                q = Q()
                for c in content_types:
                    q |= Q(pk=c.pk)
                ct_l = Content_type.objects.filter(q)
                att_l = Attribute_type.objects.filter(content_type__in=ct_l)

        #compile attribute dictionary
        att_dict = {}
        for a in att_l:
            if str(a.pk) not in att_dict:
                att_dict[str(a.pk)] = [a.name,a.short_name]

        #create column headers
        column_headers = [['Name','name',1],['Short Name','short_name',0]]
        extra_labels = {'type': 'Type','parent_source':'Parent','is_inventory':'Inv','no_folios':'#Fol'}

        if extra_headers:
            for i in extra_headers:
                column_headers.append([extra_labels[i],i,1])
        for id, names in att_dict.items():
            if id in def_headers:
                column_headers.append([names[0],names[1],1])
            else:
                column_headers.append([names[0],names[1],0])

        return column_headers


class SourceCreate(CreateView):
    model = Source
    form_class = forms.source_main
    template_name_suffix = "_create_form"

@method_decorator(login_required,name='dispatch')
class SourceDetail(View):
    """
    Container for views of individual Source objects. A GET request will
    display the source, while a POST request will be a form handler to update
    the source.
    """

    def get(self, request, *args, **kwargs):
        """Display the source"""
        view = SourceDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Update the source"""
        view = SourceUpdate.as_view()
        return view(request, *args, **kwargs)

class SourceDisplay(DetailView):
    model = Source

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = ['Repository', 'Inventories']
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context = functions.set_menus(self.request, context, state)
        context['page_title'] = self.object.name
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
                'dom': '''"<'sub-card-header clearfix'<'card-header-title'>Br><'card-body'tip>"''',
                'stateSave': 'true',
                'select': 'true',
                'paging': 'true',
                'language': '{searchPlaceholder: "Search..."}',
                'order': [[ 3, "asc" ]]
                }
            context['table_buttons_pages'] = [
                '{ extend: "colvis", text: "\uf0db", className: "dt-buttons-subcard dt-buttons-corner-right" }',
                #'{ extend: "create", text: "\uf067", editor: editor }',
                #'{ extend: "edit", text: "\uf304", editor: editor }',
                #'{ extend: "remove", text: "\uf00d", editor: editor }'
                ]

        if has_children:
            context['children'] = self.object.source_set.all().order_by('name')
            context['table_options_children'] = {
                'pageLength':5,
                'responsive':'true',
                'dom': '''"<'sub-card-header clearfix'<'card-header-title'>Br><'card-body'tip>"''',
                'stateSave': 'true',
                'select': 'true',
                'paging': 'true',
                'language': '{searchPlaceholder: "Search..."}'
                }
            context['table_buttons_children'] = [
                '{ extend: "colvis", text: "\uf0db", className: "dt-buttons-subcard dt-buttons-corner-right" }',
                #'{ extend: "create", text: "\uf067", editor: editor }',
                #'{ extend: "edit", text: "\uf304", editor: editor }',
                #'{ extend: "remove", text: "\uf00d", editor: editor }'
                ]

        return context

    def get_object(self):
        """
        Raise a 404 on things that aren't proper UUIDs,
        which would normally raise an exception.
        """
        try:
            # Call the superclass
            object = super().get_object()
            return object
        except:
            raise Http404

class SourceUpdate(UpdateView):
    model = Source
    template_name_suffix = '_update_form'
    form_class = forms.source_main

def SourceManifest(request, pk):
    context = {}
    source = Source.objects.get(pk=pk)
    context['source'] = source
    context['page_canvases'] = [page.get_canvas() for page in source.pages.all()]
    return render(request, 'dalme_app/source_manifest.html', context)

def PageManifest(request, pk):
    context = {}
    page = Page.objects.get(pk=pk)
    context['page'] = page
    context['canvas'] = page.get_canvas()
    return render(request, 'dalme_app/page_manifest.html', context)

@method_decorator(login_required,name='dispatch')
class ImageDetail(DetailView):
    model = rs_resource
    template_name = 'dalme_app/image_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = ['Repository', 'Images']
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context = functions.set_menus(self.request, context, state)
        context['page_title'] = 'DAM Image ' + str(self.object.ref)

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
                label = rs_resource_type_field.objects.get(ref=a.resource_type_field).title
                dict = {
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
            dict = {
                'id': col.ref,
                'name': col.name,
                'creator': functions.get_dam_user(col.user, 'html'),
                'path': col.theme+' ≫ '+col.theme2+' ≫ '+col.theme3,
            }
            collections.append(dict)

        context['collections'] = collections

        context['table_options'] = {
            'pageLength':5,
            'responsive':'true',
            'dom': '''"<'sub-card-header clearfix'<'card-header-title'>Br><'card-body'tip>"''',
            'stateSave': 'true',
            'select': 'true',
            'paging': 'true',
            'language': '{searchPlaceholder: "Search..."}',
            }
        context['table_buttons'] = [
            '{ extend: "colvis", text: "\uf0db" }',
            ]

        context['image_url'] = functions.get_dam_preview(self.object.ref)

        return context

    def get_object(self):
        """
        Raise a 404 on things that aren't proper UUIDs,
        which would normally raise an exception.
        """
        try:
            # Call the superclass
            object = super().get_object()
            return object
        except:
            raise Http404


@method_decorator(login_required,name='dispatch')
class ImageList(DTListView):
    page_title = 'Image List'
    breadcrumb = ['Repository','Images']
    table_options = {
        'pageLength':25,
        'responsive':'true',
        'dom': '''"<'card-table-header'B<'#filters-button-ct.dt-buttons'>fr><'#filters-container.collapse.clearfix'><'card-table-body'tip>"''',
        'serverSide': 'true',
        'stateSave': 'true',
        'deferRender': 'true',
        'language': '{searchPlaceholder: "Search"}'
        }
    ajax_string = '"../api/images/?format=json"'
    table_buttons = [
        '{ extend: "colvis", text: "\uf0db" }',
        '"pageLength"',
        ]
    column_headers = [
            ['DAM Id','ref',1],
            ['Title','field8',1],
            ['Folio','field79',1],
            ['Image','has_image',1],
            ['Date','field12',0],
            ['Created','creation_date',0],
            ['Creator','created_by',0],
            ['Country','field3',0],
            ['Collections','collections',1],
            ['Original filename','field51',0],
            ]
    render_dict = {
            'Image': '''function ( data, type, row, meta ) {return data == true ? '<i class="fa fa-check-circle dt_checkbox_true"></i>' : '<i class="fa fa-times-circle dt_checkbox_false"></i>';}''',
            'Date': '''function ( data ) {return moment(data).format("DD-MMM-YYYY");}''',
            'Created': '''function ( data ) {return moment(data).format("DD-MMM-YYYY@HH:mm");}''',
            'DAM Id': '''function ( data, type, row, meta ) {return (typeof data == 'undefined') ? "" : '<a href="'+data.url+'">'+data.ref+'</a>';}''',
            'Creator': '''function ( data, type, row, meta ) { var isnum = /^\\d+$/.test(data); return isnum == false ? '<a href="/user/'+data+'">'+data+'</a>' : data ;}''',
            }
    filters = [
        {
            'label':'Title',
            'field':'field8',
            'type':'text',
            'operator':'and',
            'lookups':[
                {'label':'is', 'lookup':'exact'},
                {'label':'contains', 'lookup':'contains'},
                {'label':'in', 'lookup':'in'},
                {'label':'starts with', 'lookup':'startswith'},
                {'label':'ends with', 'lookup':'endswith'},
                {'label':'matches regex', 'lookup':'regex'},
            ],
        },
        {
            'label':'Has Image',
            'field':'has_image',
            'type':'switch',
            'operator':'and',
        },
    ]
    countries = rs_resource.objects.filter(resource_type=1, archive=0).values('field3').distinct()
    collections = rs_collection.objects.all().values('name').distinct()
    c_filter = {
            'label':'Country',
            'field':'field3',
            'type':'check',
            'operator':'or',
        }
    col_filter = {
            'label':'Collections',
            'field':'collections',
            'type':'select',
            'operator':'or',
        }
    filters = functions.add_filter_options(countries, c_filter, filters, 'check')
    filters = functions.add_filter_options(collections, col_filter, filters)

@method_decorator(login_required,name='dispatch')
class PageMain(View):
    def get(self, request, *args, **kwargs):
        """Display list of pages"""
        view = PageList.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handle creating new pages"""
        view = PageCreate.as_view()
        return view(request, *args, **kwargs)

@method_decorator(login_required,name='dispatch')
class PageList(DTListView):
    breadcrumb = ['Repository','Pages']
    page_title = 'Page List'
    table_options = {
        'pageLength':25,
        'responsive':'true',
        'dom': '''"<'card-table-header'Bfr><'card-table-body'tip>"''',
        'serverSide': 'true',
        'stateSave': 'true',
        'deferRender': 'true',
        'language': '{searchPlaceholder: "Search..."}'
        }
    ajax_string = '"../api/pages/?format=json"'
    table_buttons = [
        '{ extend: "colvis", text: "\uf0db" }',
        '"pageLength"',
        ]
    column_headers = [
            ['Name', 'name', 1],
            ['DAM Id', 'dam_id', 1],
            ['Order','order', 1]
            ]
    #render_dict = {
    #        'Image': '''function ( data, type, row, meta ) {return data == true ? '<i class="fa fa-check-circle dt_checkbox_true"></i>' : '<i class="fa fa-times-circle dt_checkbox_false"></i>';}''',
    #        'Date': '''function ( data ) {return moment(data).format("DD-MMM-YYYY");}''',
    #        'Created': '''function ( data ) {return moment(data).format("DD-MMM-YYYY@HH:mm");}''',
    #        'DAM Id': '''function ( data, type, row, meta ) {return (typeof data == 'undefined') ? "" : '<a href="'+data.url+'">'+data.ref+'</a>';}''',
    #        }

@method_decorator(login_required,name='dispatch')
class PageDetail(View):
    def get(self, request, *args, **kwargs):
        """Display list of sources"""
        view = PageDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handle creating new sources"""
        view = PageUpdate.as_view()
        return view(request, *args, **kwargs)

class PageDisplay(DetailView):
    model = Page
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        breadcrumb = ['Pages']
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context = functions.set_menus(self.request, context, state)
        context['page_title'] = self.object.name
        context['form'] = forms.page_main(instance=self.object)
        return context

class PageUpdate(UpdateView):
    model = Page
    form_class = forms.page_main
    template_name_suffix = '_update_form'

class PageCreate(CreateView):
    model = Page
    form_class = forms.page_main
    template_name_suffix = '_create_form'

@method_decorator(login_required,name='dispatch')
class Index(TemplateView):
    template_name = 'dalme_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = ['Dashboard']
        try:
            sidebar_toggle = self.request.session['sidebar_toggle']
        except:
            self.request.session['sidebar_toggle'] = ''
            sidebar_toggle = self.request.session['sidebar_toggle']
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['sidebar_toggle'] = sidebar_toggle
        context = functions.set_menus(self.request, context, state)
        context['tiles'] = menu_constructor(self.request, 'tile_item', 'home_tiles_default.json', state)
        context['page_title'] = 'DALME Dashboard'

        return context

@method_decorator(login_required,name='dispatch')
class UIRefMain(View):
    """
    Routes requests to UIRef views
    """
    def get(self, request, *args, **kwargs):
        if 'm' in self.request.GET:
            template = 'UI_reference/'+self.request.GET['m']+'.html'
            breadcrumb = ['UI Reference', self.request.GET['m'].capitalize()]
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
        context['page_title'] = 'DALME UI Reference'

        return context

@method_decorator(login_required,name='dispatch')
class Scripts(TemplateView):
    template_name = 'dalme_app/scripts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = ['Dev Scripts']
        sidebar_toggle = self.request.session['sidebar_toggle']
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['sidebar_toggle'] = sidebar_toggle
        context = functions.set_menus(self.request, context, state)
        context['scripts'] = custom_scripts.get_script_menu()
        context['page_title'] = 'Dev Scripts'
        if 's' in self.request.GET:
            scpt = self.request.GET['s']
            context['output'] = eval('custom_scripts.'+scpt+'()')
        return context
