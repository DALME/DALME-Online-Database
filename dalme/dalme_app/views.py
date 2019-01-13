"""
Functions for managing views
"""

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connections
from django.db.models import Q, Count, F
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.template.defaulttags import register
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.base import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from django_celery_results.models import TaskResult

import requests, uuid, os, datetime
from allaccess.views import OAuthCallback

from dalme_app import functions, scripts, forms
from dalme_app.menus import menu_constructor
from dalme_app.models import (par_inventory, par_folio, par_token, par_object,
    error_message, Agent, Attribute_type, Attribute, Attribute_DATE,
    Attribute_DBR, Attribute_INT, Attribute_STR, Attribute_TXT, Concept,
    Content_class, Content_type, Content_type_x_attribute_type, Headword,
    Object, Object_attribute, Place, Source, Page, Transcription,
    Identity_phrase, Object_phrase, Word_form, Token,
    Identity_phrase_x_entity, Profile)
from dalme_app.tasks import parse_inventory

@register.filter
def get_item(obj, key):
    try:
        return obj.get(key)
    except AttributeError:
        return getattr(obj,key)

#authentication (sub)classses
class OAuthCallback_WP(OAuthCallback):

    def get_or_create_user(self, provider, access, info):
        uname = info['user_login']
        email = info['email']
        name = info['display_name']
        User = get_user_model()
        try:
            the_user = User.objects.get(username=uname)
        except Entry.DoesNotExist:
            the_user = User.objects.create_user(uname, email, None)
            the_user.profile.full_name = name
            the_user.save()

        return the_user

@method_decorator(login_required,name='dispatch')
class SourceMain(View):
    """
    Collects views to be displayed from the root of sources. GET requests to
    this endpoint will list sources, while POST requests will handle creating
    new sources.
    """

    def get(self, request, *args, **kwargs):
        """Display list of sources"""
        view = SourceListDT.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handle creating new sources"""
        view = SourceCreate.as_view()
        return view(request, *args, **kwargs)

class SourceListDT(TemplateView):
    template_name = 'dalme_app/generic_list_DT.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "List of Sources"
        context['class'] = 'source'
        context['dropdowns'] = menu_constructor('dropdown_item', 'dropdowns_default.json')
        context['sidebar'] = menu_constructor('sidebar_item', 'sidebar_default.json')
        context['columns'] = ['name','type','is_inventory','parent_source']
        #context['object_properties'] = ['type','is_inventory','parent_source','no_attributes','attribute_list']
        context['create_form'] = forms.source_main()
        context['table_options'] = ['pageLength: 25', 'responsive: true', 'paging: true', 'processing: true', 'serverSide: true']

        if 'type' in self.request.GET:
            context['type'] = self.request.GET['type']
        else:
            context['type'] = ""

        if 'order' in self.request.GET:
            context['order'] = self.request.GET['order']

        return context


class DataTableProvider(BaseDatatableView):
    # State the model the table should draw data from, or implement method "get_initial_queryset"
    #model = Source
    # define the columns that will be shown
    columns = ['name','type','is_inventory','parent_source']
    # define columns that will be used for sorting
    # keep same order as "columns" use empty string (i.e. '') for non-sortable columns
    order_columns = ['name', 'type', 'is_inventory', '']
    # set max limit of records returned, this is a security feature
    #max_display_length = 20

    def get_initial_queryset(self):
        #get entire queryset
        queryset = Source.objects.all()

        # get valid types
        types = {}
        for type in Content_type.objects.all():
            types[type.name] = type.pk

        if 'type' in self.request.GET:
            q_obj = Q()
            type_filters = self.request.GET['type'].split('|')
            for filter in type_filters:
                if filter in types:
                    q_obj |= Q(type=types[filter])
                elif filter == "inv":
                    q_obj &= Q(is_inventory=True)
            #queryset = Source.objects.filter(q_obj).annotate(no_attributes=Count('attributes'))
            queryset = Source.objects.filter(q_obj)

        if 'order' in self.request.GET:
            # do something to change the order
            pass
        else:
            queryset = queryset.order_by('type','short_name')

        return queryset

    def filter_queryset(self, qs):
        # use request parameters to filter queryset

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(name__istartswith=search)

        return qs


class SourceList(ListView):
    # TODO: Different columns for different filters
    # TODO: Filter for is_inventory boolean field
    # TODO: Allow for dynamic ordering
    #paginate_by = 20
    template_name = 'dalme_app/generic_list.html'
    #queryset = Source.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "List of Sources"
        context['class_single'] = "source"
        context['dropdowns'] = menu_constructor('dropdown_item', 'dropdowns_default.json')
        context['sidebar'] = menu_constructor('sidebar_item', 'sidebar_default.json')
        context['object_properties'] = ['type','is_inventory','parent_source','no_attributes']
        #context['object_properties'] = ['type','is_inventory','parent_source','no_attributes','attribute_list']
        context['create_form'] = forms.source_main()

        if 'type' in self.request.GET:
            context['type'] = self.request.GET['type']
        else:
            context['type'] = ""
        if 'order' in self.request.GET:
            context['order'] = self.request.GET['order']
        return context

    def get_queryset(self):
        # get entire queryset
        #queryset = Source.objects.all()
        #test_source = Source.objects.get(pk='1abc52313988415192a0749282be2523')
        #test_attributes = test_source.attributes.all()
        #test_ct = test_source.type.attribute_list
        #queryset = Source.objects.annotate(
        #    no_attributes=Count('attributes'),
        #    test=F('attributes__attribute_date__value'),
        #    test2=self.annotate('john')
        #    )
        #queryset = Source.objects.annotate(
        #    no_attributes=Count('attributes'),
        #    test2=self.attributes.all()
        #    )

        # get valid types
        types = {}
        for type in Content_type.objects.all():
            types[type.name] = type.pk

        if 'type' in self.request.GET:
            q_obj = Q()
            type_filters = self.request.GET['type'].split('|')
            for filter in type_filters:
                if filter in types:
                    q_obj |= Q(type=types[filter])
                elif filter == "inv":
                    q_obj &= Q(is_inventory=True)
            queryset = Source.objects.filter(q_obj).annotate(no_attributes=Count('attributes'))
            #queryset = Source.objects.filter(q_obj)

        if 'order' in self.request.GET:
            # do something to change the order
            pass
        else:
            queryset = queryset.order_by('type','short_name')

        return queryset

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
        context['source_has_children'] = len(self.object.source_set.all()) > 0
        context['source_has_pages'] = len(self.object.page_set.all()) > 0
        context['children'] = self.object.source_set.all().order_by('name')
        context['dropdowns'] = menu_constructor('dropdown_item', 'dropdowns_default.json')
        context['sidebar'] = menu_constructor('sidebar_item', 'sidebar_default.json')
        context['page_title'] = self.object.name
        context['form'] = forms.source_main(instance=self.object)
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
        context['dropdowns'] = menu_constructor('dropdown_item', 'dropdowns_default.json')
        context['sidebar'] = menu_constructor('sidebar_item', 'sidebar_default.json')
        context['page_title'] = self.object.name
        context['form'] = forms.page_main(instance=self.object)
        return context

class PageList(ListView):
    model = Page
    template_name = "dalme_app/generic_list.html"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['dropdowns'] = menu_constructor('dropdown_item', 'dropdowns_default.json')
        context['sidebar'] = menu_constructor('sidebar_item', 'sidebar_default.json')
        context['create_form'] = forms.page_main()
        context['page_title'] = "Page List"
        return context

class PageUpdate(UpdateView):
    model = Page
    form_class = forms.page_main
    template_name_suffix = '_update_form'

class PageCreate(CreateView):
    model = Page
    form_class = forms.page_main
    template_name_suffix = '_create_form'

@login_required
def index(request):
    context = {
            'page_title':'DALME Dashboard',
            'authenticated': request.user.is_authenticated,
            'username': request.user.username,
            'sidebar': menu_constructor('sidebar_item', 'sidebar_default.json'),
            'dropdowns': menu_constructor('dropdown_item', 'dropdowns_default.json'),
            'tiles': menu_constructor('tile_item', 'home_tiles_default.json'),
            'chart_data': functions.bar_chart(),
        }

    return render(request, 'index.html', context)

@login_required
def search(request):

    return render(request, 'search.html', context)

@login_required
def uiref(request, module):
    context = {
            'page_title':'DALME Dashboard Demo',
            'authenticated': request.user.is_authenticated,
            'username': request.user.username,
            'sidebar': menu_constructor('sidebar_item', 'sidebar_default.json'),
            'dropdowns': menu_constructor('dropdown_item', 'dropdowns_default.json'),
        }

    _url = 'UI_reference/{}.html'.format(module)

    return render(request, _url, context)

@login_required
def list(request, module, type='all'):
    _url = 'list.html'
    table_options = ''
    username = request.user.username
    context = {}
    if module == 'sources':
        _title = 'DALME Dashboard | Sources'
        _heading = 'Sources'
        panel_icon = 'fa-list'
        context['has_actions'] = 1
        context['actions'] = (
            ('href="#import" data-toggle="modal" data-target="#import"', 'Add new source'),
            ('divider', ' '),
            ('href="#"', 'Action 2'),
            ('href="#"', 'Action 3'),
        )
        context['has_modals'] = 1
        context['modals'] = [
            ('import', [
                'Add New Source',
                'form',
                'Submit',
                'type="submit" form="import-form"'
            ]),
        ]

        if request.method == 'POST':
            form = forms.upload_file(request.POST, request.FILES)

            if form.is_valid():
                #ingest_inventory should check the file's format and look at the metadata
                check = functions.inventory_check(form.cleaned_data['inv_file'])
                #missing structure section
                if check['has_structure'] == 0:
                    functions.notification(request, 4002)

                else:
                    #missing transcription section
                    if check['has_transcription'] == 0:
                        functions.notification(request, 3001)

                    #prep metadata form
                    #if missing metadata section entirely
                    if check['has_metadata'] == 0:
                        req_text = 'The file is missing the METADATA section, please input the relevant information below.'
                    #if missing required fields
                    elif check['required'] == 0:
                        req_text = 'Required information is missing from the METADATA section in the file, please complete the fields highlighted below.'
                    #if it's all there and this is just to verify
                    else:
                        req_text = 'The information below was extracted from the METADATA section of the file, please verify that the information is correct. If not, then change it accordingly.'

                    check['req_text'] = req_text
                    request.session['form_data'] = check

                    # redirect to inventory metadata form:
                    return HttpResponseRedirect('/form/inventory_metadata')

            else:
                functions.notification(request, 4003, data=form.errors)
        else:
            form = forms.upload_file()

        context['form'] = form
        types = Content_type.objects.filter(content_class=1)
        types_dict = {}
        for t in types:
            types_dict[t.id] = t.name

        if type == 'all':
            panel_title = 'List of all sources'
            headers = ['Type', 'Title']
            sources_list = Source.objects.all().order_by('type','short_name')
            rows = []

            for i in sources_list:
                tr_class = ''

                if i.type.pk <= 11:
                    title = i.short_name
                else:
                    title = i.name

                type = types_dict.get(i.type,'n/a')
                row = [tr_class, (
                    '<td>' + type + '</td>',
                    '<td><a href="/show/source/' + str(i.id) + '">' + title + '</a></td>',
                    )
                ]
                rows.append(row)

        elif type == 'notarial':
            panel_title = 'List of notarial sources (acts and registers)'

        elif type == 'inventories':
            panel_title = 'List of inventories'
            headers = ['Type', 'Title','Start Date','End Date','Source']
            inventories = Source.objects.filter(is_inventory=True).order_by('short_name')
            dates_list = Attribute_DATE.objects.select_related('attribute_id').filter(Q(attribute_id__attribute_type=25) | Q(attribute_id__attribute_type=26))
            types_list = Attribute_STR.objects.select_related('attribute_id').filter(attribute_id__attribute_type=28)


        elif type == 'biblio':
            panel_title = 'List of bibliographic sources'
            headers = ['Type', 'Title']
            biblio_sources = Source.objects.filter(type__lte=11).order_by('short_name')
            attribute_list = Attribute_STR.objects.select_related('attribute_id').filter(Q(attribute_id__attribute_type=15) | Q(attribute_id__attribute_type=1))
            rows = []

            for i in biblio_sources:
                tr_class = ''
                title = i.name + '</a>'
                atts = attribute_list.filter(attribute_id__content_id=i.id)
                if atts:
                    lang_buttons = ''
                    for a in atts:
                        language = a.value
                        l_button = '<div class="list_inrow_button">' + language + '</div>'
                        lang_buttons = lang_buttons + l_button
                    title = title + lang_buttons

                type = types_dict.get(i.type,'n/a')
                row = [tr_class, (
                    '<td>' + type + '</td>',
                    '<td><a href="/show/source/' + str(i.id) + '">' + title + '</td>',
                    )
                ]
                rows.append(row)

        elif type == 'archives':
            panel_title = 'List of archives and collections'


    elif module == 'errors':
        _title = 'DALME Dashboard | Errors and Notifications'
        _heading = 'Errors and Notifications'
        panel_title = 'List of error and notification codes'
        panel_icon = 'fa-medkit'
        context['has_actions'] = 1
        context['actions'] = (
            ('href="#addNew" data-toggle="modal" data-target="#addNew"', 'Add New'),
            ('divider', ' '),
            ('title', 'Filter by level:'),
            ('href="#"', 'Debug'),
            ('href="#"', 'Info'),
            ('href="#"', 'Success'),
            ('href="#"', 'Warning'),
            ('href="#"', 'Error'),
        )
        context['has_modals'] = 1
        context['modals'] = [
            ('addNew', [
                'Add New Code',
                'form',
                'Submit',
                'type="submit" form="addNew-form"'
            ]),
        ]

        if request.method == 'POST':
            form = new_error(request.POST)

            if form.is_valid():
                # process the data in form.cleaned_data as required
                e_level = form.cleaned_data['e_level']
                e_type = form.cleaned_data['e_type']
                e_text = form.cleaned_data['e_text']
                e_code = functions.get_new_error(e_level)

                message = error_message(
                    e_code = e_code,
                    e_level = e_level,
                    e_type = e_type,
                    e_text = e_text
                    )
                message.save()

                functions.notification(request, 2503, para={ 'code': str(e_code) })

                # redirect to a new URL:
                return HttpResponseRedirect('/list/errors')

            else:
                functions.notification(request, 4003, data=form.errors)
        else:
            form = new_error()

        context['form'] = form
        headers = ['Code', 'Level', 'Type', 'Text']
        errors = error_message.objects.all()
        rows = []

        for i in errors:
            d_code = str(i.e_code)
            d_level = i.get_e_level_display()
            d_type = i.get_e_type_display()
            d_text = i.e_text

            tr_class = ''
            row = [tr_class, (
                '<td>' + d_code + '</td>',
                '<td>' + d_level + '</td>',
                '<td>' + d_type + '</td>',
                '<td>' + d_text + '</td>')
            ]
            rows.append(row)

    elif module == 'objects':
        _title = 'DALME Dashboard | List Objects'
        _heading = 'Objects'
        panel_title = 'List of Objects'
        panel_icon = 'fa-beer'
        context['has_actions'] = 1
        context['actions'] = (
            ('href="#"', 'Action 2'),
            ('href="#"', 'Action 3'),
        )
        headers = ['Object ID', 'Name', 'Class', 'Material', 'Room', 'Terms']
        objects = par_object.objects.all()
        rows = []
        for i in objects:
            tr_class = ''
            row = [tr_class, (
                '<td>' + str(i.obj_id) + '</td>',
                '<td>' + i.name + '</td>',
                '<td>' + i.ont_class + '</td>',
                '<td>' + i.material + '</td>',
                '<td>' + i.room + '</td>',
                '<td>' + i.terms + '</td>')
            ]
            rows.append(row)

    elif module == 'tasks':
        _title = 'DALME Dashboard | Background Tasks Manager'
        _heading = 'Background Tasks'
        panel_title = 'List of Task Results'
        panel_icon = 'fa-tasks'
        context['has_actions'] = 1
        context['actions'] = (
            ('href="#"', 'Action 2'),
            ('href="#"', 'Action 3'),
        )
        table_options = 'pageLength: 50'
        headers = ['Task No.', 'Date', 'Status']
        tasks = TaskResult.objects.all().order_by('status')
        rows = []
        for i in tasks:
            if i.status == 'FAILURE':
                tr_class = 'danger'
            else:
                tr_class = ''

            row = [
                tr_class, ('<td>' + str(i.id) + '</td>',
                '<td>' + str(i.date_done) + '</td>',
                '<td>' + i.status + '</td>')
            ]
            rows.append(row)

    elif module == 'users':
        _title = 'DALME Dashboard | Users'
        _heading = 'Users'
        panel_title = 'List of users'
        panel_icon = 'fa-users'
        context['has_actions'] = 1
        context['actions'] = (
            ('href="#addNew" data-toggle="modal" data-target="#addNew"', 'Add New'),
        )
        context['has_modals'] = 1
        context['modals'] = [
            ('addNew', [
                'Add New User',
                'form',
                'Submit',
                'type="submit" form="addNew-form"'
            ]),
        ]

        if request.method == 'POST':
            form = new_user(request.POST)

            if form.is_valid():
                functions.create_user(request, form)
                functions.notification(request, 2502)
                # redirect to a new URL:
                return HttpResponseRedirect('/list/users')

            else:
                functions.notification(request, 4003, data=form.errors)
        else:
            form = new_user()

        context['form'] = form
        headers = ['Username', 'Name', 'Email', 'Staff', 'Superuser', 'DAM Usergroup', 'Wiki Groups', 'WP Role']
        users = User.objects.all().select_related('profile')
        rows = []

        for i in users:
            d_username = i.username
            d_name = i.profile.full_name
            d_email = i.email
            d_staff = str(i.is_staff)
            d_superuser = str(i.is_superuser)
            d_dam = i.profile.get_dam_usergroup_display()
            d_wiki = i.profile.wiki_groups
            d_wp = str(i.profile.get_wp_role_display())

            tr_class = ''
            row = [tr_class, (
                '<td>' + d_username + '</td>',
                '<td>' + d_name + '</td>',
                '<td>' + d_email + '</td>',
                '<td>' + d_staff + '</td>',
                '<td>' + d_superuser + '</td>',
                '<td>' + d_dam + '</td>',
                '<td>' + d_wiki + '</td>',
                '<td>' + d_wp + '</td>')
            ]
            rows.append(row)

    else:
        functions.notification(request, 4004)
        return HttpResponseRedirect('/')

    context['page_title'] = _title
    context['authenticated'] = request.user.is_authenticated
    context['username'] = username
    context['item'] = 'THIS IS WHERE ITEM TITLE GOES'
    context['heading'] = _heading
    context['sidebar'] = menu_constructor('sidebar_item', 'sidebar_default.json')
    context['dropdowns'] = menu_constructor('dropdown_item', 'dropdowns_default.json')
    context['headers'] = headers
    context['rows'] = rows
    context['panel_title'] = panel_title
    context['panel_icon'] = panel_icon
    context['table_options'] = table_options

    return render(request, _url, context)


@login_required
def show(request, item, id):
    username = request.user.username
    context = {}
    if item == 'inventory':
        id = uuid.UUID(id).hex
        inv = par_inventory.objects.get(pk=id)
        folios = inv.par_folio_set.all()

        if not folios:
            functions.notification(request, 4001)
            return HttpResponseRedirect('/list/inventories')

        else:
            context['page_title'] = 'DALME Dashboard | Inventory ' + inv.title
            context['heading'] = inv.title
            context['has_actions'] = 1
            context['actions'] = (
                ('href="javascript:change_autorefreshdiv();"', 'Tokenise'),
                ('divider', ' '),
                ('href="#"', 'Do something else'),
                ('href="#"', 'Yay!'),
            )
            _url = 'show_inventory.html'
            inventory = functions.get_inventory(inv, 'full')
            page = request.GET.get('page', 1)
            pages = Paginator(inventory, 1)

            try:
                folios = pages.page(page)

            except PageNotAnInteger:
                folios = pages.page(1)

            except EmptyPage:
                folios = pages.page(paginator.num_pages)

            context['authenticated'] = request.user.is_authenticated
            context['username'] = request.user.username
            context['item'] = item.title()
            context['sidebar'] = menu_constructor('sidebar_item', 'sidebar_default.json')
            context['dropdowns'] = menu_constructor('dropdown_item', 'dropdowns_default.json')
            context['inventory'] = inventory
            context['folios'] = folios

    return render(request, _url, context)

@login_required
def form(request, item):
    username = request.user.username
    context = {}
    form_data = request.session.get('form_data')

    if item == 'inventory_metadata':
        _title = 'DALME Dashboard | Inventory Metadata'
        _heading = 'Inventory Metadata'
        panel_title = 'Metadata'
        panel_icon = 'fa-list'
        _url = 'inventory_metadata.html'
        req_text = form_data['req_text']
        if request.method == 'POST':
            form = inventory_metadata(request.POST)

            if form.is_valid():
                #create inventory record in database
                inv = par_inventory(
                    title=form.cleaned_data['inv_title'],
                    source=form.cleaned_data['inv_source'],
                    location=form.cleaned_data['inv_location'],
                    series=form.cleaned_data['inv_series'],
                    shelf=form.cleaned_data['inv_shelf'],
                    transcriber=form.cleaned_data['inv_transcriber'],
                    creation_username=username,
                    modification_username=username
                    )
                inv.save()
                inv_id = str(inv.id)
                #call parser to process content in parallel thread
                task = parse_inventory.delay(form_data, inv_id, username)
                task_id = task.id

                #redirect to inventories list with status message
                functions.notification(request, 2001)
                return HttpResponseRedirect('/list/inventories')

            else:
                functions.notification(request, 4003, data=form.errors)

        else:
            ini_data = form_data['metadata']
            ini_data['inv_title'] = ini_data.pop('Title')
            ini_data['inv_source'] = ini_data.pop('Archival source')
            ini_data['inv_location'] = ini_data.pop('Country')
            ini_data['inv_series'] = ini_data.pop('Series')
            ini_data['inv_shelf'] = ini_data.pop('Shelf')
            ini_data['inv_transcriber'] = ini_data.pop('Transcriber')
            form = inventory_metadata(initial=ini_data)

    context['page_title'] = _title
    context['authenticated'] = request.user.is_authenticated
    context['username'] = username
    context['heading'] = _heading
    context['sidebar'] = menu_constructor('sidebar_item', 'sidebar_default.json')
    context['dropdowns'] = menu_constructor('dropdown_item', 'dropdowns_default.json')
    context['panel_title'] = panel_title
    context['panel_icon'] = panel_icon
    context['form'] = form
    context['req_text'] = req_text

    return render(request, _url, context)

@login_required
def script(request, module):
    username = request.user.username
    output = eval('scripts.' + module + '(request, username)')

    context = {
            'page_title':'DALME Script Results',
            'authenticated': request.user.is_authenticated,
            'username': request.user.username,
            'sidebar': menu_constructor('sidebar_item', 'sidebar_default.json'),
            'dropdowns': menu_constructor('dropdown_item', 'dropdowns_default.json'),
            'heading': module,
            'output': output
        }

    _url = 'script_results.html'

    return render(request, _url, context)

@login_required
def iiif(request, module):
    if module == 'diva':
        url = 'iiif_test_diva.html'
    elif module == 'mirador':
        url = 'iiif_test_mirador.html'

    context = {
            'page_title':'DALME IIIF Viewer Test',
            'authenticated': request.user.is_authenticated,
            'username': request.user.username,
            'sidebar': menu_constructor('sidebar_item', 'sidebar_default.json'),
            'dropdowns': menu_constructor('dropdown_item', 'dropdowns_default.json'),
        }

    return render(request, _url, context)
