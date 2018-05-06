from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests, uuid
from .menus import sidebar_menu, dropdowns
from .forms import upload_file, new_error, inventory_metadata
from dalme_app import functions, scripts
from .models import par_inventories, par_folios, par_tokens, par_objects, error_messages, Agents, Attribute_types, Attributes, Attributes_DATE, Attributes_DBR, Attributes_INT, Attributes_STR, Attributes_TXT, Concepts, Content_classes, Content_types, Content_types_x_attribute_types, Headwords, Objects, Object_attributes, Places, Sources, Pages, Transcriptions, Identity_phrases, Object_phrases, Word_forms, Tokens, Identity_phrases_x_entities
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dalme_app.tasks import parse_inventory
from django_celery_results.models import TaskResult
from django.db.models import Q

#import re

@login_required
def index(request):
    inv_counter = str(functions.get_count('inventories'))
    obj_counter = str(functions.get_count('objects'))
    wiki_counter = str(functions.get_count('wiki-articles'))
    dam_counter = str(functions.get_count('assets'))

    context = {
            'page_title':'DALME Dashboard',
            'authenticated': request.user.is_authenticated,
            'username': request.user.username,
            'sidebar': sidebar_menu(),
            'dropdowns': dropdowns(request.user.username),
            'chart_data': functions.bar_chart(),
            'inv_counter': inv_counter,
            'obj_counter': obj_counter,
            'wiki_counter': wiki_counter,
            'dam_counter': dam_counter,
        }

    return render(request, 'index.html', context)

@login_required
def uiref(request, module):
    context = {
            'page_title':'DALME Dashboard Demo',
            'authenticated': request.user.is_authenticated,
            'username': request.user.username,
            'sidebar': sidebar_menu(),
            'dropdowns': dropdowns(request.user.username)
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
            form = upload_file(request.POST, request.FILES)

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
            form = upload_file()

        context['form'] = form
        types = Content_types.objects.filter(content_class=1)
        types_dict = {}
        for t in types:
            types_dict[t.id] = t.name

        if type == 'all':
            panel_title = 'List of all sources'
            headers = ['Type', 'Title']
            sources_list = Sources.objects.all().order_by('type','short_name')
            rows = []

            for i in sources_list:
                tr_class = ''

                if i.type <= 11:
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
            inventories = Sources.objects.filter(is_inventory=True).order_by('short_name')
            dates_list = Attributes_DATE.objects.select_related('attribute_id').filter(Q(attribute_id__attribute_type=25) | Q(attribute_id__attribute_type=26))
            types_list = Attributes_STR.objects.select_related('attribute_id').filter(attribute_id__attribute_type=28)


        elif type == 'biblio':
            panel_title = 'List of bibliographic sources'
            headers = ['Type', 'Title']
            biblio_sources = Sources.objects.filter(type__lte=11).order_by('short_name')
            attribute_list = Attributes_STR.objects.select_related('attribute_id').filter(Q(attribute_id__attribute_type=15) | Q(attribute_id__attribute_type=1))
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

                message = error_messages(
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
        errors = error_messages.objects.all()
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
        objects = par_objects.objects.all()
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

    context['page_title'] = _title
    context['authenticated'] = request.user.is_authenticated
    context['username'] = username
    context['item'] = 'THIS IS WHERE ITEM TITLE GOES'
    context['heading'] = _heading
    context['sidebar'] = sidebar_menu()
    context['dropdowns'] = dropdowns(request.user.username)
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
        inv = par_inventories.objects.get(pk=id)
        folios = inv.par_folios_set.all()

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
            context['sidebar'] = sidebar_menu()
            context['dropdowns'] = dropdowns(request.user.username)
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
                inv = par_inventories(
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
    context['sidebar'] = sidebar_menu()
    context['dropdowns'] = dropdowns(request.user.username)
    context['panel_title'] = panel_title
    context['panel_icon'] = panel_icon
    context['form'] = form
    context['req_text'] = req_text

    return render(request, _url, context)

@login_required
def script(request, module):
    username = request.user.username
    output = eval('scripts.' + module + '(username)')

    context = {
            'page_title':'DALME Script Results',
            'authenticated': request.user.is_authenticated,
            'username': request.user.username,
            'sidebar': sidebar_menu(),
            'dropdowns': dropdowns(request.user.username),
            'heading': module,
            'output': output
        }

    _url = 'script_results.html'

    return render(request, _url, context)
