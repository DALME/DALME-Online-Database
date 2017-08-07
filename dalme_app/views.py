from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.contrib import messages
#from .models import predicates, tokens, sources, predicate_labels, source_attributes
import requests
from .menus import sidebar_menu
from .forms import upload_inventory, new_error
from dalme_app import functions
from .models import par_inventories, par_folios, par_tokens, error_messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#import re

def index(request):
    context = {
            'page_title':'DALME Dashboard',
            'authenticated': request.user.is_authenticated,
            'username': request.user.username,
            'sidebar': sidebar_menu()
        }

    return render(request, 'index.html', context)


def uiref(request, module):
    context = {
            'page_title':'DALME Dashboard Demo',
            'authenticated': request.user.is_authenticated,
            'username': request.user.username,
            'sidebar': sidebar_menu()
        }

    if module == 'dash_demo':
        _url = 'UI_reference/dash_demo.html'

    elif module == 'panels-wells':
        _url = 'UI_reference/panels-wells.html'

    elif module == 'buttons':
        _url = 'UI_reference/buttons.html'

    elif module == 'notifications':
        _url = 'UI_reference/notifications.html'

    elif module == 'typography':
        _url = 'UI_reference/typography.html'

    elif module == 'icons':
        _url = 'UI_reference/icons.html'

    elif module == 'grid':
        _url = 'UI_reference/grid.html'

    elif module == 'tables':
        _url = 'UI_reference/tables.html'

    elif module == 'flot':
        _url = 'UI_reference/flot.html'

    elif module == 'morris':
        _url = 'UI_reference/morris.html'

    elif module == 'forms':
        _url = 'UI_reference/forms.html'

    #messages.add_message(request, messages.INFO, 'Currently in DEMO mode.')

    return render(request, _url, context)

def list(request, item):
    _url = 'list.html'
    username = request.user.username
    context = {}
    if item == 'inventories':
        _title = 'DALME Dashboard | List Inventories'
        _heading = 'Inventories'
        panel_title = 'List of inventories'
        panel_icon = 'fa-list'
        context['has_actions'] = 1
        context['actions'] = (
            ('href="#import" data-toggle="modal" data-target="#import"', 'Import Inventory'),
            ('divider', ' '),
            ('href="#"', 'Action 2'),
            ('href="#"', 'Action 3'),
        )
        context['has_modals'] = 1
        context['modals'] = [
            ('import', [
                'Import Inventory',
                'form',
                'Submit',
                'type="submit" form="import-form"'
            ]),
        ]

        if request.method == 'POST':
            form = upload_inventory(request.POST, request.FILES)

            if form.is_valid():
                # process the data in form.cleaned_data as required
                result_status = functions.ingest_inventory(form.cleaned_data['inv_file'], username)
                #for i in result_status:
                    #functions.notification(request, i)
                messages.add_message(request, messages.SUCCESS, 'Everything peachy')
                # redirect to a new URL:
                return HttpResponseRedirect('/dashboard/list/inventories')
            else:
                messages.add_message(request, messages.ERROR, 'Problem!' + str(form.errors))
        else:
            form = upload_inventory()

        context['form'] = form
        headers = ['Title', 'Source', 'Location', 'Series', 'Shelf', 'Transcriber']
        inventories = par_inventories.objects.all()
        rows = []
        for i in inventories:
            row = [
                '<td><a href="/dashboard/show/inventory/' + i._id + '">' + i.title + '</a></td>',
                '<td>' + i.source + '</td>',
                '<td>' + i.location + '</td>',
                '<td>' + i.series + '</td>',
                '<td>' + i.shelf + '</td>',
                '<td>' + i.transcriber + '</td>'
            ]
            rows.append(row)

    elif item == 'errors':
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

                messages.add_message(request, messages.INFO, 'Message added. The new error code is ' + str(e_code) + '.')
                # redirect to a new URL:
                return HttpResponseRedirect('/dashboard/list/errors')
            else:
                messages.add_message(request, messages.ERROR, form.errors)
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

            row = [
                '<td>' + d_code + '</td>',
                '<td>' + d_level + '</td>',
                '<td>' + d_type + '</td>',
                '<td>' + d_text + '</td>'
            ]
            rows.append(row)

    context['page_title'] = _title
    context['authenticated'] = request.user.is_authenticated
    context['username'] = username
    context['item'] = item.title()
    context['heading'] = _heading
    context['sidebar'] = sidebar_menu()
    context['headers'] = headers
    context['rows'] = rows
    context['panel_title'] = panel_title
    context['panel_icon'] = panel_icon

    return render(request, _url, context)

def show(request, item, _id):
    username = request.user.username
    context = {}
    if item == 'inventory':
        inv = par_inventories.objects.get(pk=_id)
        folios = inv.par_folios_set.all()

        if not folios:
            functions.notification(request, 4001)
            return HttpResponseRedirect('/dashboard/list/inventories')

        else:
            context['page_title'] = 'DALME Dashboard | Inventory ' + inv.title
            context['heading'] = inv.title
            context['has_actions'] = 1
            context['actions'] = (
                ('href="#addNew" data-toggle="modal" data-target="#addNew"', 'Tokenise'),
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
            context['inventory'] = inventory
            context['folios'] = folios

    return render(request, _url, context)

#def index(request):
#    latest_sources = sources.objects.order_by('-modification_timestamp')[:5]
#    the_tokens = tokens.objects.order_by('-modification_timestamp')[:5]
#    context = {
#        'page_title':'DALME | Home',
#        'sources': latest_sources,
#        'tokens': the_tokens,
#        'authenticated': request.user.is_authenticated
#    }
#    return render(request, 'dalme_app/index.html', context)

#def source_detail(request, source_id):
#    getty_term = request.GET.get('set_getty_to', '')
#    concept = get_object_or_404(PlatonicConcept, pk=concept_id)
#    context = {'concept': concept, 'authenticated': request.user.is_authenticated}
#    if getty_term != '':
#        if request.user.is_authenticated:
#            concept.getty_term = getty_term
#            concept.save()
#        return HttpResponseRedirect(reverse('concept_detail', kwargs={'concept_id': concept_id}))
#    else:
#        if hasattr(concept, 'getty_term') and concept.getty_term != None and concept.getty_term != "":
#            url = 'http://vocab.getty.edu/sparql.json'
#            Q = {
#                '_implicit': 'false',
#                'implicit': 'true',
#                '_equivalent': 'false',
#                '_form': '%2Fsparql'
#            }
#            lookup_value = "aat:" + re.findall(r'aat/([0-9]+)',concept.getty_term)[0]
#            query = "select ?l ?lab ?lang ?pref ?historic ?display ?pos ?type ?kind ?flag ?start ?end ?comment {\
#              values ?s {%s}\
#              values ?pred {xl:prefLabel xl:altLabel}\
#              ?s ?pred ?l.\
#              bind (if(exists{?s gvp:prefLabelGVP ?l},\"pref GVP\",if(?pred=xl:prefLabel,\"pref\",\"\")) as ?pref)\
#              ?l xl:literalForm ?lab.\
#              optional {?l dct:language [gvp:prefLabelGVP [xl:literalForm ?lang]]}\
#              optional {?l gvp:displayOrder ?ord}\
#              optional {?l gvp:historicFlag [skos:prefLabel ?historic]}\
#              optional {?l gvp:termDisplay [skos:prefLabel ?display]}\
#              optional {?l gvp:termPOS [skos:prefLabel ?pos]}\
#              optional {?l gvp:termType [skos:prefLabel ?type]}\
#              optional {?l gvp:termKind [skos:prefLabel ?kind]}\
#              optional {?l gvp:termFlag [skos:prefLabel ?flag]}\
#              optional {?l gvp:estStart ?start}\
#              optional {?l gvp:estEnd ?end}\
#              optional {?l rdfs:comment ?comment}\
#            } order by ?ord" % lookup_value
#            Q['query'] = query
#            R = requests.get(url, params=Q)
#            R.encoding = 'utf=8'
#            getty_info = R.json()['results']['bindings']
#            context['getty_info'] = getty_info
#        return render(request, 'dalme_app/concept_detail.html', context)

#def dropdown_test(request):
#    dropdown_items = sources.objects.order_by('dropdown_content')[:60]
#    context = {
#        'page_title':'DALME | Dropdown Test',
#        'menu': dropdown_items,
#        'authenticated': request.user.is_authenticated
#    }
#    return render(request, 'dalme_app/dropdown_test.html', context)
