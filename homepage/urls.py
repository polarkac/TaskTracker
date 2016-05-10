from django.conf.urls import url

from homepage.views import LoginView, LogoutView

urlpatterns = [
    url(r'logout/$', LogoutView.as_view(), name='homepage-logout'),
    url(r'$', LoginView.as_view(), name='homepage-login'),
]
