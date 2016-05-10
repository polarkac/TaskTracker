from django.conf.urls import url

from homepage.views import HomepageView

urlpatterns = [
    url(r'', HomepageView.as_view()),
]
