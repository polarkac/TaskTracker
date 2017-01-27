from django.views.generic import (
    TemplateView, CreateView, DeleteView, RedirectView, UpdateView
)
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from tasks.models import (
    Project, Task, Comment, TimeLog, TaskState, Category, Priority
)
from tasks.forms import ProjectForm, CommentTimeLogForm
from tasks.utils import (
    get_total_project_spend_time, annotate_total_time_per_task,
    LoginRequired,
)

class ProjectDetailView(LoginRequired, TemplateView):

    template_name = 'tasks/project_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        project = self.get_project()
        tasks = self.get_tasks(project)
        total_project_spend_time = get_total_project_spend_time(tasks)
        unpaid_tasks = Task.objects.filter(project=project, paid=False)
        total_project_payment = 0
        for task in unpaid_tasks:
            total_project_payment += task.get_payment()

        page = self.request.GET.get('page')
        paginator = Paginator(tasks, 15)
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)
        annotate_total_time_per_task(tasks)

        context.update({
            'project': project, 'tasks': tasks,
            'total_project_spend_time': total_project_spend_time,
            'total_project_payment': total_project_payment,
        })

        return context

    def get_project(self):
        user = self.request.user
        try:
            pk = int(self.kwargs.get('pk'))
            project = get_object_or_404(Project, id=pk, user=user)
        except ValueError:
            project = None

        return project

    def get_tasks(self, project):
        tasks = Task.objects.filter(project=project).select_related()

        return tasks

class ProjectCreateView(LoginRequired, CreateView):

    model = Project
    template_name = 'tasks/project_form.html'
    form_class = ProjectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})

        return kwargs

    def get_success_url(self):
        return reverse('tasks-project-detail', args=[self.object.id])

class ProjectDeleteView(LoginRequired, DeleteView):

    model = Project
    template_name = 'tasks/project_delete_confirm.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        user = self.request.user
        obj = get_object_or_404(Project, id=pk, user=user, default=False)

        return obj

    def get_success_url(self):
        return reverse('tasks-home')

class TasksHomeView(LoginRequired, TemplateView):

    template_name = 'tasks/tasks_home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.request.user
        general_project = Project.objects.get(name='General', user=user)
        not_closed_states = TaskState.objects.exclude(name='Closed')
        tasks = (
            Task.objects.filter(project__user=user, state=not_closed_states)
            .select_related()
        )
        total_project_spend_time = get_total_project_spend_time(tasks)
        tasks = tasks[:15]
        annotate_total_time_per_task(tasks)
        context.update({
            'project': general_project, 'tasks': tasks,
            'total_project_spend_time': total_project_spend_time,
        })

        return context

class TaskCreateView(LoginRequired, CreateView):

    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['name', 'description', 'per_hour', 'priority', 'category']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({'project': self.get_project()})

        return context

    def get_initial(self):
        task_category = Category.objects.get(name='Task')
        normal_priority = Priority.objects.get(name='Normal')

        return {'category': task_category, 'priority': normal_priority}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.project = self.get_project()
        self.object.state = TaskState.objects.get(name='New')
        self.object.save()

        return super().form_valid(form)

    def get_project(self):
        user = self.request.user
        id = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=id, user=user)

        return project

    def get_success_url(self):
        return reverse('tasks-project-detail', args=[self.object.project.id])

class TaskDetailView(LoginRequired, TemplateView):

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
        task = get_object_or_404(Task, id=pk, project__user=user)

        return task

    def get_comments(self):
        comments = (
            Comment.objects.all().filter(task=self.task).select_related('timelog')
        )

        return comments

    def get_comment_time_log_form(self):
        initial = {'state': self.task.state.id}
        if self.request.method == 'POST':
            comment_time_log_form = CommentTimeLogForm(
                self.request.POST, initial=initial
            )
        else:
            comment_time_log_form = CommentTimeLogForm(initial=initial)

        return comment_time_log_form

class TaskChangePaidView(LoginRequired, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        url = self.request.GET.get('next')

        return url

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self._change_paid()

        return response

    def _change_paid(self):
        task_pk = self.kwargs.get('task_pk')
        task = Task.objects.get(id=task_pk)
        task.paid = False if task.paid else True
        task.save()

class TaskUpdateView(LoginRequired, UpdateView):

    model = Task
    fields = ['name', 'description', 'priority', 'category', 'per_hour']
    template_name = 'tasks/task_form.html'
    pk_url_kwarg = 'task_pk'

    def get_success_url(self):
        return reverse('tasks-task-detail', args=[self.object.id])

class ProjectUpdateView(LoginRequired, UpdateView):

    model = Project
    fields = ['name', 'description']
    template_name = 'tasks/project_form.html'

    def get_success_url(self):
        return reverse('tasks-project-detail', args=[self.object.id])
