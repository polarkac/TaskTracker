from django.conf.urls import url

from tasks.views import TaskCreateView

urlpatterns = [
    url(
        r'^create/(?P<project_pk>[0-9]+)/$', TaskCreateView.as_view(),
        name='tasks-task-create'
    ),
]
