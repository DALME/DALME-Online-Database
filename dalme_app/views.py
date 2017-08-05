from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.contrib import messages
#from .models import predicates, tokens, sources, predicate_labels, source_attributes
import requests
from .menus import sidebar_menu
from .forms import upload_inventory
from dalme_app import functions
from .models import par_inventories, par_folios, par_tokens
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#import re

def index(request):
    context = {
            'page_title':'DALME Dashboard',
            'authenticated': request.user.is_authenticated,
            'sidebar': sidebar_menu()
        }

    return render(request, 'index.html', context)


def uiref(request, module):
    context = {
            'page_title':'DALME Dashboard Demo',
            'authenticated': request.user.is_authenticated,
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

def upload(request, item):
    _url = 'upload.html'
    if item == 'inventory':
        _title = 'DALME Dashboard | Upload Inventory'
        _heading = 'Data Upload'
        if request.method == 'POST':
            form = upload_inventory(request.POST, request.FILES)

            if form.is_valid():
                # process the data in form.cleaned_data as required
                result_status = functions.ingest_inventory(request.FILES['inv_file'])
                for i in result_status['messages']:
                    m = i[0]
                    _level = functions.get_error_level(i[1])
                    messages.add_message(request, _level, m)

                # redirect to a new URL:
                return HttpResponseRedirect('/dashboard/')
            else:
                messages.add_message(request, messages.ERROR, 'Problem!' + str(form.errors))
        else:
            form = upload_inventory()

    context = {
            'page_title': _title,
            'authenticated': request.user.is_authenticated,
            'item': item.title(),
            'heading': _heading,
            'sidebar': sidebar_menu(),
            'form': form
        }

    return render(request, _url, context)


def list(request, item):
    _url = 'list.html'
    if item == 'inventories':
        _title = 'DALME Dashboard | List Inventories'
        _heading = 'Inventories'
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

    context = {
            'page_title': _title,
            'authenticated': request.user.is_authenticated,
            'item': item.title(),
            'heading': _heading,
            'sidebar': sidebar_menu(),
            'headers': headers,
            'rows': rows
        }

    return render(request, _url, context)

def show(request, item, _id):

    if item == 'inventory':
        inv = par_inventories.objects.get(pk=_id)
        _title = 'DALME Dashboard | Inventory ' + inv.title
        _heading = inv.title
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

        context = {
            'page_title': _title,
            'authenticated': request.user.is_authenticated,
            'item': item.title(),
            'heading': _heading,
            'sidebar': sidebar_menu(),
            'inventory': inventory,
            'folios': folios,
        }

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
