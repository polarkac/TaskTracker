from django.views.generic import TemplateView, CreateView, DeleteView
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.db.models import Sum

from tasks.models import Project, Task, Comment, TimeLog
from tasks.forms import ProjectForm, CommentTimeLogForm

class ProjectDetailView(TemplateView):

    template_name = 'tasks/project_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            project = self.get_project()
        except Project.DoesNotExist:
            raise Http404
        tasks = self.get_tasks(project)

        context.update({'project': project, 'tasks': tasks})

        return context

    def get_project(self):
        user = self.request.user
        try:
            pk = int(self.kwargs.get('pk'))
            project = Project.objects.get(id=pk, user=user)
        except ValueError:
            project = None

        return project

    def get_tasks(self, project):
        tasks = Task.objects.filter(project=project)

        return tasks

class ProjectCreateView(CreateView):

    model = Project
    template_name = 'tasks/project_form.html'
    form_class = ProjectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})

        return kwargs

    def get_success_url(self):
        return reverse('tasks-project-detail', args=[self.object.id])

class ProjectDeleteView(DeleteView):

    model = Project
    template_name = 'tasks/project_delete_confirm.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        user = self.request.user
        try:
            obj = Project.objects.get(id=pk, user=user, default=False)
        except Project.DoesNotExist:
            raise Http404

        return obj

    def get_success_url(self):
        return reverse('tasks-home')

class TasksHomeView(TemplateView):

    template_name = 'tasks/tasks_home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.request.user
        general_project = Project.objects.get(name='General', user=user)
        tasks = Task.objects.filter(project__user=user)\
            .order_by('-created_date').select_related()[:10]
        context.update({'project': general_project, 'tasks': tasks})

        return context

class TaskCreateView(CreateView):

    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['name', 'description', 'priority', 'category']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({'project': self.get_project()})

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.project = self.get_project()
        self.object.save()

        return super().form_valid(form)

    def get_project(self):
        user = self.request.user
        try:
            self.project = Project.objects.get(
                pk=self.kwargs.get('project_pk'), user=user
            )
        except Project.DoesNotExist:
            raise Http404

        return self.project

    def get_success_url(self):
        return reverse('tasks-project-detail', args=[self.project.id])

class TaskDetailView(TemplateView):

    template_name = 'tasks/task_detail.html'

    def get(self, request, *args, **kwargs):
        self.task = self.get_task()
        comment_time_log_form = self.get_comment_time_log_form()

        return self.render_to_response(self.get_context_data(
            comment_time_log_form=comment_time_log_form
        ))

    def post(self, request, *args, **kwargs):
        self.task = self.get_task()
        comment_time_log_form = self.get_comment_time_log_form()
        if comment_time_log_form.is_valid():
            comment_time_log_form.save(self.task)
            response = HttpResponseRedirect(reverse(
                'tasks-task-detail', args=[self.task.id]
            ))
        else:
            response = self.render_to_response(
                self.get_context_data(comment_time_log_form=comment_time_log_form)
            )

        return response

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        comments = self.get_comments()
        total_spend_time = (
            TimeLog.objects.filter(comment__task=self.task)
            .aggregate(Sum('spend_time'))
        )['spend_time__sum']
        context.update({
            'task': self.task, 'comments': comments,
            'total_spend_time': total_spend_time,
        })

        return context

    def get_task(self):
        pk = self.kwargs.get('task_pk')
        user = self.request.user
        try:
            task = Task.objects.get(id=pk, project__user=user)
        except Task.DoesNotExist:
            raise Http404

        return task

    def get_comments(self):
        comments = (
            Comment.objects.all().filter(task=self.task).select_related('timelog')
        )

        return comments

    def get_comment_time_log_form(self):
        if self.request.method == 'POST':
            comment_time_log_form = CommentTimeLogForm(self.request.POST)
        else:
            comment_time_log_form = CommentTimeLogForm()

        return comment_time_log_form
