from django.views.generic import FormView, RedirectView
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout

class LoginView(FormView):

    template_name = 'homepage/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tasks-project-detail', args=['general'])

class LogoutView(RedirectView):

    permanent = False
    pattern_name = 'homepage-login'

    def get_redirect_url(self, *args, **kwargs):
        self._logout_user()

        return super().get_redirect_url(*args, **kwargs)

    def _logout_user(self):
        if self.request.user.is_authenticated():
            logout(self.request)
