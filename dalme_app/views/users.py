from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView
from dalme_app.utils import DALMEMenus as dm
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from ._common import DALMEListView, get_page_chain
from dalme_app.forms import preference_form_builder
from dalme_app.forms import UserPreferenceForm
from django.conf import settings


@method_decorator(login_required, name='dispatch')
class UserList(DALMEListView):
    """ Lists users and allows editing and creation of new records via the API """
    page_title = 'Users'
    dt_config = 'users'
    breadcrumb = [('System', ''), ('Users', '/users/')]
    helpers = ['user_forms']


@method_decorator(login_required, name='dispatch')
class UserDetail(FormMixin, DetailView):
    model = User
    template_name = 'dalme_app/user_detail.html'
    form_class = UserPreferenceForm

    def get_form_class(self, *args, **kwargs):
        form_class = preference_form_builder(self.form_class, instance=self.request.user)
        return form_class

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetail, self).get_context_data(*args, **kwargs)
        context['api_endpoint']: settings.API_ENDPOINT
        if self.request.GET.get('preferences') is not None:
            context['preferences'] = True
        breadcrumb = [('System', ''), ('Users', '/users')]
        sidebar_toggle = self.request.user.preferences['interface__sidebar_collapsed']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = self.object.profile.full_name
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        user_data = {
            'First name': self.object.first_name,
            'Last name': self.object.last_name,
            'User ID': self.object.id,
            'Email': '<a href="mailto:{}">{}</a>'.format(self.object.email, self.object.email),
            'Staff': '<i class="fa fa-check-circle dt_checkbox_true"></i>' if self.object.is_staff else '<i class="fa fa-times-circle dt_checkbox_false"></i>',
            'Superuser': '<i class="fa fa-check-circle dt_checkbox_true"></i>' if self.object.is_superuser else '<i class="fa fa-times-circle dt_checkbox_false"></i>',
            'Active': '<i class="fa fa-check-circle dt_checkbox_true"></i>' if self.object.is_active else '<i class="fa fa-times-circle dt_checkbox_false"></i>',
            'Joined': timezone.localtime(self.object.date_joined).strftime('%d %B, %Y @ %H:%M').lstrip("0").replace(" 0", " "),
            'Last login': timezone.localtime(self.object.last_login).strftime('%d %B, %Y @ %H:%M').lstrip("0").replace(" 0", " "),
            'Groups': ', '.join([i.name for i in self.object.groups.all()])
        }
        context['user_data'] = user_data
        context['image_url'] = self.object.profile.profile_image
        context['form'] = self.get_form()
        context['section_list'] = [i[0] for i in self.form_class.registry.section_objects.items()]
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        form.update_preferences()
        return super(UserDetail, self).form_valid(form)

    def get_object(self):
        try:
            object = User.objects.get(username=self.kwargs['username'])
            return object
        except ObjectDoesNotExist:
            raise Http404
