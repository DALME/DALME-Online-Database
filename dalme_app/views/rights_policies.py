from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from dalme_app.models import RightsPolicy
from django.core.exceptions import ObjectDoesNotExist
from ._common import DALMEListView, DALMEDetailView


@method_decorator(login_required, name='dispatch')
class RightsList(DALMEListView):
    page_title = 'Rights Policies'
    dt_config = 'rights'
    breadcrumb = [('Project', ''), ('Rights Policies', '/rights')]


@method_decorator(login_required, name='dispatch')
class RightsDetail(DALMEDetailView):
    model = RightsPolicy
    template_name = 'dalme_app/generic_detail.html'
    breadcrumb = [('Project', ''), ('Rights Policies', '/rights')]
    page_title = 'Policy'
    comments = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notice_disp = '<i class="fas fa-check-square"></i>' if self.object.notice_display else '<i class="far fa-square"></i>'
        object_attributes = {
            'ID': self.object.id,
            'Name': self.object.name,
            'Rights Holder': self.object.rights_holder,
            'Rights Status': self.object.get_rights_status_display(),
            'Rights': self.object.rights,
            'Notice Display': notice_disp,
            'Rights Notice': self.object.rights_notice,
            'Licence': self.object.licence
        }
        if self.object.attachments:
            object_attributes.update({
                'Attachment': '<a href="/download/{}">{}</a>'.format(self.object.attachments.file, self.object.attachments.filename)
            })

        context.update({
            'object_class': 'Rights Policy',
            'object_icon': 'fas fa-copyright',
            'attribute_dictionaries': 'Rights Notice',
            'object_attributes': object_attributes
        })

        return context

    def get_object(self):
        try:
            object = RightsPolicy.objects.get(pk=self.kwargs['pk'])
            return object
        except ObjectDoesNotExist:
            raise Http404
