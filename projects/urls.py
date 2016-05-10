from django.conf.urls import url

from projects.views import ProjectsListView, ProjectCreateView, ProjectDeleteView

urlpatterns = [
    url(r'list/$', ProjectsListView.as_view(), name='projects-list'),
    url(r'create/$', ProjectCreateView.as_view(), name='projects-create'),
    url(
        r'delete/(?P<pk>[0-9]+)/$', ProjectDeleteView.as_view(),
        name='projects-delete'
    ),
]
