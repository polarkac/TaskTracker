from django.conf.urls import url

from tasks.views import TaskCreateView, TasksHomeView, TaskDetailView

urlpatterns = [
    url(r'^home/$', TasksHomeView.as_view(), name='tasks-home'),
    url(
        r'^create/(?P<project_pk>[0-9]+)/$', TaskCreateView.as_view(),
        name='tasks-task-create'
    ),
    url(
        r'^detail/(?P<task_pk>[0-9]+)/$', TaskDetailView.as_view(),
        name='tasks-task-detail'
    ),
]
