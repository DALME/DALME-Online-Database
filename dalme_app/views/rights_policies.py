import json
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from dalme_app.utils import DALMEMenus as dm
from dalme_app.models import RightsPolicy
from django.core.exceptions import ObjectDoesNotExist
from ._common import DALMEListView, get_page_chain
from django.conf import settings


@method_decorator(login_required, name='dispatch')
class RightsList(DALMEListView):
    page_title = 'Rights Policies'
    dt_config = 'rights'
    breadcrumb = [('Project', ''), ('Rights Policies', '/rights')]


@method_decorator(login_required, name='dispatch')
class RightsDetail(DetailView):
    model = RightsPolicy
    template_name = 'dalme_app/generic_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_endpoint']: settings.API_ENDPOINT
        breadcrumb = [('Project', ''), ('Rights Policies', '/rights')]
        sidebar_toggle = self.request.user.preferences['interface__sidebar_collapsed']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = 'Policy: ' + self.object.name
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        context['object_class'] = 'Rights Policy'
        context['object_icon'] = 'fas fa-copyright'
        context['comments'] = 'RightsPolicy'
        if self.object.notice_display:
            notice_disp = '<i class="fas fa-check-square"></i>'
        else:
            notice_disp = '<i class="far fa-square"></i>'
        context['attribute_dictionaries'] = ['Rights Notice']
        context['object_attributes'] = {
            'ID': self.object.id,
            'Name': self.object.name,
            'Rights Holder': self.object.rights_holder,
            'Rights Status': self.object.get_rights_status_display(),
            'Rights': self.object.rights,
            'Notice Display': notice_disp,
            'Rights Notice': self.object.rights_notice,
            'Licence': self.object.licence,
            'Attachment': '<a href="/download/{}">{}</a></div></div>'.format(self.object.attachments.file, self.object.attachments.filename)
        }
        return context

    def get_object(self):
        try:
            object = RightsPolicy.objects.get(pk=self.kwargs['pk'])
            return object
        except ObjectDoesNotExist:
            raise Http404
