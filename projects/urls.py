from django.conf.urls import url

from projects.views import ProjectsListView

urlpatterns = [
    url(r'list/$', ProjectsListView.as_view(), name='projects-list'),
]
