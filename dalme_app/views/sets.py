from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import View
from dalme_app.models import RightsPolicy, Set, Source
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from ._common import DALMEListView, DALMEDetailView


@method_decorator(login_required, name='dispatch')
class SetList(DALMEListView):
    helpers = ['ownership_filter_module']
    editor = 'true'
    includes = None

    def get_config(self, *args, **kwargs):
        type = self.request.GET['type']
        return {
            'page_title': type.capitalize(),
            'dt_config': 'sets_' + type,
            'breadcrumb': [('Sets', ''), (type.capitalize(), '/sets/?type=' + type)],
            'helpers': self.helpers,
            'includes': self.includes,
            'form_template': self.form_template,
            'editor': self.editor
            }


@method_decorator(login_required, name='dispatch')
class SetsDetail(DALMEDetailView):
    model = RightsPolicy
    template_name = 'dalme_app/set_detail.html'
    breadcrumb = [('Project', ''), ('Sets', '/sets')]
    comments = True

    def get_object(self):
        try:
            object = Set.objects.get(pk=self.kwargs['pk'])
            return object
        except ObjectDoesNotExist:
            raise Http404


@method_decorator(login_required, name='dispatch')
class SetsRedirect(View):
    def get(self, request, *args, **kwargs):
        workset = get_object_or_404(Set, pk=kwargs['pk'])
        members = Source.objects.filter(sets__set_id=workset.id)
        try:
            current = members.filter(sets__workset_done=False)[0]
        except IndexError:
            current = members[-1]
        url = '/{}/{}/?set={}'.format(workset.endpoint, current.id, workset.id)
        return HttpResponseRedirect(url)
