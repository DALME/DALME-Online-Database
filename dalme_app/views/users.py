from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from ._common import DALMEListView, DALMEDetailView
from dalme_app.forms import preference_form_builder
from dalme_app.forms import UserPreferenceForm


@method_decorator(login_required, name='dispatch')
class UserList(DALMEListView):
    """ Lists users and allows editing and creation of new records via the API """
    page_title = 'Users'
    dt_config = 'users'
    breadcrumb = [('System', ''), ('Users', '/users/')]
    helpers = ['user_forms']


@method_decorator(login_required, name='dispatch')
class UserDetail(FormMixin, DALMEDetailView):
    model = User
    template_name = 'dalme_app/user_detail.html'
    form_class = UserPreferenceForm
    breadcrumb = [('System', ''), ('Users', '/users')]

    def get_form_class(self, *args, **kwargs):
        form_class = preference_form_builder(self.form_class, instance=self.request.user)
        return form_class

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetail, self).get_context_data(*args, **kwargs)
        preferences = True if self.request.GET.get('preferences') is not None else False

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

        context.update({
            'preferences': preferences,
            'user_data': user_data,
            'image_url': self.object.profile.profile_image,
            'form': self.get_form(),
            'section_list': [i[0] for i in self.form_class.registry.section_objects.items()]
        })

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

    def get_page_title(self):
        return self.object.profile.full_name

    def get_object(self):
        try:
            object = User.objects.get(username=self.kwargs['username'])
            return object
        except ObjectDoesNotExist:
            raise Http404
