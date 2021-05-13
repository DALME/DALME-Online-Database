from django.contrib.auth.views import LoginView


class DalmeLogin(LoginView):
    """ Overwrites LoginView method to allow users to be redirected accross subdomains on login """
    def get_redirect_url(self):
        """Return the user-originating redirect URL"""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        return redirect_to

    def get_success_url(self):
        self.set_session_prefs()
        return super().get_success_url()

    def set_session_prefs(self):
        self.request.session['sidebar_toggle'] = self.request.user.preferences['interface__sidebar_collapsed']
        self.request.session['remember_columns'] = self.request.user.preferences['interface__remember_column_visibility']
        self.request.session['list_scope'] = self.request.user.preferences['interface__records_list_scope']
