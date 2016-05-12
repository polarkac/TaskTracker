from django.conf.urls import url

from tasks.views import ProjectDetailView, ProjectCreateView, ProjectDeleteView

urlpatterns = [
    url(
        r'^detail/(?P<pk>([0-9]+|general))/$', ProjectDetailView.as_view(),
        name='tasks-project-detail'
    ),
    url(r'^create/$', ProjectCreateView.as_view(), name='tasks-project-create'),
    url(
        r'^delete/(?P<pk>[0-9]+)/$', ProjectDeleteView.as_view(),
        name='tasks-project-delete'
    ),
]
