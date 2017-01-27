from django.conf.urls import url

from tasks.views import (
    ProjectDetailView, ProjectCreateView, ProjectDeleteView, ProjectUpdateView,
)

urlpatterns = [
    url(
        r'^detail/(?P<pk>[0-9]+)/$', ProjectDetailView.as_view(),
        name='tasks-project-detail'
    ),
    url(r'^create/$', ProjectCreateView.as_view(), name='tasks-project-create'),
    url(
        r'^delete/(?P<pk>[0-9]+)/$', ProjectDeleteView.as_view(),
        name='tasks-project-delete'
    ),
    url(
        r'^update/(?P<pk>[0-9]+)/$', ProjectUpdateView.as_view(),
        name='tasks-project-update'
    ),
]
