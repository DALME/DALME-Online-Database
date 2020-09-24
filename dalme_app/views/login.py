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
