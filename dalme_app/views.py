from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import PlatonicConcept, Relationship, Source

import requests
import re

def index(request):
    latest_concepts = PlatonicConcept.objects.order_by('-modification_timestamp')[:5]
    relationships = Relationship.objects.order_by('-modification_timestamp')[:5]
    context = {
        'page_title':'DALME | Home',
        'concepts': latest_concepts,
        'relationships': relationships,
        'authenticated': request.user.is_authenticated
    }
    return render(request, 'dalme_app/index.html', context)

def concept_detail(request, concept_id):
    getty_term = request.GET.get('set_getty_to', '')
    concept = get_object_or_404(PlatonicConcept, pk=concept_id)
    context = {'concept': concept, 'authenticated': request.user.is_authenticated}
    if getty_term != '':
        if request.user.is_authenticated:
            concept.getty_term = getty_term
            concept.save()
        return HttpResponseRedirect(reverse('concept_detail', kwargs={'concept_id': concept_id}))
    else:
        if hasattr(concept, 'getty_term') and concept.getty_term != None and concept.getty_term != "":
            url = 'http://vocab.getty.edu/sparql.json'
            Q = {
                '_implicit': 'false',
                'implicit': 'true',
                '_equivalent': 'false',
                '_form': '%2Fsparql'
            }
            lookup_value = "aat:" + re.findall(r'aat/([0-9]+)',concept.getty_term)[0]
            query = "select ?l ?lab ?lang ?pref ?historic ?display ?pos ?type ?kind ?flag ?start ?end ?comment {\
              values ?s {%s}\
              values ?pred {xl:prefLabel xl:altLabel}\
              ?s ?pred ?l.\
              bind (if(exists{?s gvp:prefLabelGVP ?l},\"pref GVP\",if(?pred=xl:prefLabel,\"pref\",\"\")) as ?pref)\
              ?l xl:literalForm ?lab.\
              optional {?l dct:language [gvp:prefLabelGVP [xl:literalForm ?lang]]}\
              optional {?l gvp:displayOrder ?ord}\
              optional {?l gvp:historicFlag [skos:prefLabel ?historic]}\
              optional {?l gvp:termDisplay [skos:prefLabel ?display]}\
              optional {?l gvp:termPOS [skos:prefLabel ?pos]}\
              optional {?l gvp:termType [skos:prefLabel ?type]}\
              optional {?l gvp:termKind [skos:prefLabel ?kind]}\
              optional {?l gvp:termFlag [skos:prefLabel ?flag]}\
              optional {?l gvp:estStart ?start}\
              optional {?l gvp:estEnd ?end}\
              optional {?l rdfs:comment ?comment}\
            } order by ?ord" % lookup_value
            Q['query'] = query
            R = requests.get(url, params=Q)
            R.encoding = 'utf=8'
            getty_info = R.json()['results']['bindings']
            context['getty_info'] = getty_info
        return render(request, 'dalme_app/concept_detail.html', context)

def dropdown_test(request):
    dropdown_items = Source.objects.order_by('dropdown_content')[:60]
    context = {
        'page_title':'DALME | Dropdown Test',
        'menu': dropdown_items,
        'authenticated': request.user.is_authenticated
    }
    return render(request, 'dalme_app/dropdown_test.html', context)
