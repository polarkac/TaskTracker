from django.views.generic import FormView, RedirectView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout

class LoginView(FormView):

    template_name = 'homepage/login.html'
    form_class = AuthenticationForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse('projects-list'))
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse('projects-list'))
        else:
            return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('projects-list')

class LogoutView(RedirectView):

    permanent = False
    pattern_name = 'homepage-login'

    def get_redirect_url(self, *args, **kwargs):
        print('redirect')
        self._logout_user()

        return super().get_redirect_url(*args, **kwargs)

    def _logout_user(self):
        if self.request.user.is_authenticated():
            logout(self.request)
