from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView
from dalme_app.utils import DALMEMenus as dm
from dalme_app.models import RightsPolicy, Set, Source
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from ._common import DALMEListView, get_page_chain


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
class SetsDetail(DetailView):
    model = RightsPolicy
    template_name = 'dalme_app/set_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Project', ''), ('Sets', '/sets')]
        sidebar_toggle = self.request.user.preferences['interface__sidebar_collapsed']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = self.object.name
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        context['set'] = self.object
        context['comments_count'] = self.object.comments.count()
        members = self.object.members.all()
        context['members'] = members
        context['tables'] = ['members', 'fa-plus-square', 'Set Members ({})'.format(members.count())]
        return context

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
