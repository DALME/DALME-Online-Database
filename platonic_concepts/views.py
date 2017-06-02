from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import PlatonicConcept, Relationship

def index(request):
    latest_concepts = PlatonicConcept.objects.order_by('-modification_timestamp')[:5]
    relationships = Relationship.objects.order_by('-modification_timestamp')[:5]
    context = {'page_title':'DALME | Home', 'concepts': latest_concepts, 'relationships': relationships}
    return render(request, 'platonic_concepts/index.html', context)

def concept_detail(request, concept_id):
    concept = get_object_or_404(PlatonicConcept, pk=concept_id)
    return render(request, 'platonic_concepts/concept_detail.html', {'concept': concept})
