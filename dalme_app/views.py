"""
Functions for managing views
"""

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

#@register.filter
#def get_item(obj, key):
#    logger.debug("get_item called on {}, {}".format(obj, key))
#    try:
#        return obj.get(key)
#    except AttributeError:
#        return getattr(obj,key)

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
        context['dropdowns'] = menu_constructor('dropdown_item', 'dropdowns_default.json', state)
        context['sidebar'] = menu_constructor('sidebar_item', 'sidebar_default.json', state)
        context['page_title'] = 'Search Results'

        return context

class GenericListView(TemplateView):
    template_name = 'dalme_app/generic_list.html'
    breadcrumb = []
    table_options = {
        'pageLength':25,
        'responsive':'true',
        'paging':'true',
        'fixedHeader': 'true',
        'dom': '"Bfrtip"',
        'serverSide': 'true',
        'stateSave': 'true',
        'select': 'true',
        'language': '{searchPlaceholder: "Search..."}'
        }
    table_buttons = ['{ extend: "colvis", text: "\uf0db" }', '"pageLength"']
    column_headers = []
    render_dict = {}
    ajax_string = ''
    table_editor = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = self.get_breadcrumb()
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = menu_constructor('dropdown_item', 'dropdowns_default.json', state)
        context['sidebar'] = menu_constructor('sidebar_item', 'sidebar_default.json', state)
        context['page_title'] = self.get_page_title()
        context['columnDefs'] = self.get_column_defs()
        context['table_options'] = self.get_table_options()
        context['table_buttons'] = self.get_table_buttons()
        context['table_editor'] = self.get_table_editor()

        return context

    def get_table_options(self, *args, **kwargs):
        table_options = self.table_options
        table_options['ajax'] = self.get_table_ajax_str()
        return table_options

    def get_page_title(self, *args, **kwargs):
        if self.kwargs['title']:
            p_title = self.kwargs['title']
        else:
            p_title = 'List View'
        return p_title

    def get_table_buttons(self, *args, **kwargs):
        return self.table_buttons

    def get_breadcrumb(self, *args, **kwargs):
        return self.breadcrumb

    def get_table_editor(self, *args, **kwargs):
        return self.table_editor

    def get_column_defs(self, *args, **kwargs):
        #create column headers
        column_headers = self.column_headers
        render_dict = self.render_dict
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

class AdminUsers(GenericListView):
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

class AdminNotifications(GenericListView):
    breadcrumb = ['System','Notifications']
    table_options = {
        'pageLength':25,
        'responsive':'true',
        'paging':'true',
        'fixedHeader': 'true',
        'dom': '"Bfrtip"',
        'serverSide': 'true',
        'stateSave': 'true',
        'select': 'true',
        'language': '{searchPlaceholder: "Search..."}'
        }
    ajax_string = '"../api/notifications/?format=json"'
    table_buttons = [
        '{ extend: "colvis", text: "\uf0db" }',
        '{ extend: "create", text: "\uf067", editor: editor }',
        '{ extend: "edit", text: "\uf304", editor: editor }',
        '{ extend: "remove", text: "\uf00d", editor: editor }',
        '"pageLength"'
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
    template_name = 'dalme_app/admin_models_list.html'

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
        column_headers_classes = [
                ['ID', 'id', 1],
                ['Name','name', 1],
                ['Short name','short_name', 0],
                ['Description','description', 1]]
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
        render_dict_classes = {}
        context['dropdowns'] = menu_constructor('dropdown_item', 'dropdowns_default.json', state)
        context['sidebar'] = menu_constructor('sidebar_item', 'sidebar_default.json', state)

        context['columnDefs_content'] = self.get_column_defs(column_headers_content, render_dict_content)
        context['columnDefs_attributes'] = self.get_column_defs(column_headers_attributes, render_dict_attributes)
        context['columnDefs_classes'] = self.get_column_defs(column_headers_classes, render_dict_classes)
        context['table_options_content'] = {
            'pageLength':25,
            'responsive':'true',
            'dom': '"Bfrt"',
            'serverSide': 'true',
            'stateSave': 'true',
            'select': '{style: "single"}',
            'ajax': '"../api/models/?format=json&type=content"',
            'scrollY': '"15vh"',
            'deferRender': 'true',
            'scroller': 'true',
            'rowId': '"id"',
            'language': '{searchPlaceholder: "Search..."}'
            }
        context['table_options_attributes'] = {
            'pageLength':25,
            'responsive':'true',
            'dom': '"Bfrt"',
            'serverSide': 'true',
            'stateSave': 'true',
            'select': '{style: "single"}',
            'ajax': '"../api/models/?format=json&type=attributes"',
            'scrollY': '"30vh"',
            'deferRender': 'true',
            'scroller': 'true',
            'rowId': '"id"',
            'language': '{searchPlaceholder: "Search..."}'
            }
        context['table_options_classes'] = {
            'pageLength':25,
            'responsive':'true',
            'dom': '"Bfrt"',
            'serverSide': 'true',
            'stateSave': 'true',
            'select': '{style: "single"}',
            'ajax': '"../api/models/?format=json&type=classes"',
            'scrollY': '"15vh"',
            'deferRender': 'true',
            'scroller': 'true',
            'rowId': '"id"',
            'language': '{searchPlaceholder: "Search..."}'
            }
        context['table_buttons_content'] = ['{ extend: "colvis", text: "\uf0db", className: "btn_single" }']
        context['table_buttons_attributes'] = ['{ extend: "colvis", text: "\uf0db", className: "btn_single"}']
        context['table_buttons_classes'] = ['{ extend: "colvis", text: "\uf0db", className: "btn_single"}']
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


class SourceList(TemplateView):
    template_name = 'dalme_app/generic_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table_options = {
            'pageLength':25,
            'responsive':'true',
            'paging':'true',
            'fixedHeader': 'true',
            'dom': '"Bfrtip"',
            'serverSide': 'true',
            'stateSave': 'true',
            'language': '{searchPlaceholder: "Search..."}'
            }
        table_buttons = ['{ extend: "colvis", text: "\uf0db" }', '"pageLength"']



        if 'type' in self.request.GET:
            type = self.request.GET['type']
            context['type'] = type
            table_options['ajax'] = '"../api/sources/?format=json&type=' + type + '"'
            list_type = Content_list.objects.get(short_name=self.request.GET['type'])
            breadcrumb = ['Sources', list_type.name]
            page_title = 'List of '+list_type.name
            def_headers = list_type.default_headers.split(',')
            if list_type.extra_headers:
                extra_headers = list_type.extra_headers.split(',')
            else:
                extra_headers = []
            q_obj = Q()
            if self.request.GET['type'] == 'inventories':
                #get ALL HEADERS
                att_l = Content_type_x_attribute_type.objects.filter(content_type=13).select_related('attribute_type')
            else:
                #get ALL HEADERS
                content_types = Content_list_x_content_type.objects.filter(content_list=list_type.pk).select_related('content_type')
                q = Q()
                for c in content_types:
                    q |= Q(content_type=c.content_type)
                att_l = Content_type_x_attribute_type.objects.filter(q).select_related('attribute_type')
        else:
            context['type'] = ""
            breadcrumb = ['Sources', 'All']
            page_title = "Sources"
            def_headers = ['15']
            extra_headers = ['type']
            table_options['ajax'] = '"../api/sources/?format=json"'
            #get ALL HEADERS
            att_l = Content_type_x_attribute_type.objects.filter(content_type__content_class=1).select_related('attribute_type')
        #compile attribute dictionary
        att_dict = {}
        for a in att_l:
            if str(a.attribute_type_id) not in att_dict:
                att_dict[str(a.attribute_type_id)] = [a.attribute_type.name,a.attribute_type.short_name]
        #create column headers
        column_headers = [['Name','name',1]]
        extra_labels = {'type': 'Type','parent_source':'Parent','is_inventory':'Inv'}
        if extra_headers:
            for i in extra_headers:
                column_headers.append([extra_labels[i],i,1])
        for id, names in att_dict.items():
            if id in def_headers:
                column_headers.append([names[0],names[1],1])
            else:
                column_headers.append([names[0],names[1],0])
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
            if i[0] in ['Name', 'Web address']:
                c_dict['render'] = '''function ( data, type, row, meta ) {return '<a href="'+data.url+'">'+data.name+'</a>';}'''
            columnDefs.append(c_dict)
            col = col + 1

        context['columnDefs'] = columnDefs
        context['table_options'] = table_options
        context['table_buttons'] = table_buttons
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = menu_constructor('dropdown_item', 'dropdowns_default.json', state)
        context['sidebar'] = menu_constructor('sidebar_item', 'sidebar_default.json', state)
        context['page_title'] = page_title

        return context

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
    context_object_name = 'source'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        breadcrumb = ['Sources', 'All']
        sidebar_toggle = self.request.session['sidebar_toggle']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['source_has_children'] = len(self.object.source_set.all()) > 0
        context['source_has_pages'] = len(self.object.page_set.all()) > 0
        context['children'] = self.object.source_set.all().order_by('name')
        context['dropdowns'] = menu_constructor('dropdown_item', 'dropdowns_default.json', state)
        context['sidebar'] = menu_constructor('sidebar_item', 'sidebar_default.json', state)
        context['page_title'] = self.object.name
        context['form'] = forms.source_main(instance=self.object)
        if Transcription.objects.filter(source_id=self.object.pk).count() > 0:
            context['transcription'] = Transcription.objects.get(source_id=self.object.pk).transcription

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

def SourceManifest(request,pk):
    context = {}
    source = Source.objects.get(pk=pk)
    context['source'] = source
    context['page_canvases'] = [page.get_canvas() for page in source.page_set.all()]
    return render(request, 'dalme_app/manifest.html', context)

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
        context['dropdowns'] = menu_constructor('dropdown_item', 'dropdowns_default.json', state)
        context['sidebar'] = menu_constructor('sidebar_item', 'sidebar_default.json', state)
        context['page_title'] = self.object.name
        context['form'] = forms.page_main(instance=self.object)
        return context

class PageList(GenericListView):
    breadcrumb = ['Pages']
    table_options = {
        'pageLength':25,
        'responsive':'true',
        'paging':'true',
        'fixedHeader': 'true',
        'dom': '"Bfrtip"',
        'serverSide': 'true',
        'stateSave': 'true',
        'select': 'true',
        'language': '{searchPlaceholder: "Search..."}'
        }
    ajax_string = '"../api/pages/?format=json"'

    column_headers = [
            ['DAM ID', 'dam_id', 1],
            ['Name', 'name', 1],
            ['Order','order', 1]
            ]

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
        context['dropdowns'] = menu_constructor('dropdown_item', 'dropdowns_default.json', state)
        context['sidebar'] = menu_constructor('sidebar_item', 'sidebar_default.json', state)
        context['tiles'] = menu_constructor('tile_item', 'home_tiles_default.json', state)
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
        context['dropdowns'] = menu_constructor('dropdown_item', 'dropdowns_default.json', state)
        context['sidebar'] = menu_constructor('sidebar_item', 'sidebar_default.json', state)
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
        context['dropdowns'] = menu_constructor('dropdown_item', 'dropdowns_default.json', state)
        context['sidebar'] = menu_constructor('sidebar_item', 'sidebar_default.json', state)
        context['tiles'] = menu_constructor('tile_item', 'home_tiles_default.json', state)
        context['scripts'] = custom_scripts.get_script_menu()
        context['page_title'] = 'Dev Scripts'
        if 's' in self.request.GET:
            scpt = self.request.GET['s']
            context['output'] = eval('custom_scripts.'+scpt+'()')
        return context
