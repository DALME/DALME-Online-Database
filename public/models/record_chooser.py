"""Model record chooser data."""

from wagtailmodelchooser import Chooser, register_model_chooser

from ida.models import Record


@register_model_chooser
class RecordChooser(Chooser):
    model = Record
    modal_template = 'public/includes/source_chooser_modal.html'
    search_fields = []

    def get_queryset(self, request):
        qs = Record.objects.filter(type=13, workflow__is_public=True).order_by('name')
        if request.GET.get('search'):
            qs = qs.filter(name__icontains=request.GET['search'])
        return qs
