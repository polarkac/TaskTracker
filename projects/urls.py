from django.conf.urls import url

from projects.views import ProjectDetailView, ProjectCreateView, ProjectDeleteView

urlpatterns = [
    url(
        r'^detail/(?P<pk>([0-9]+|none))/$', ProjectDetailView.as_view(),
        name='projects-detail'
    ),
    url(r'^create/$', ProjectCreateView.as_view(), name='projects-create'),
    url(
        r'^delete/(?P<pk>[0-9]+)/$', ProjectDeleteView.as_view(),
        name='projects-delete'
    ),
]
